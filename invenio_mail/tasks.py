# SPDX-FileCopyrightText: 2015-2025 CERN.
# SPDX-FileCopyrightText: 2023-2024 University of Münster.
# SPDX-License-Identifier: MIT

"""Background tasks for mail module."""

import json
import logging
import random
import smtplib
from base64 import b64decode

from celery import shared_task
from flask import current_app
from flask_mail import Message

from .errors import AttachmentOversizeException


def send_email_with_attachments(data, attachments=None):
    """Celery task for sending mails with attachments.

    Args:
        data: A dict with the email fields.
        attachments: A list of dicts, in the following form:

            ```python
            attachments = [
                {
                    "base64": "RGllcyBpc3QgZGFzIEhhdXMgdm9tIE5pa29sYXVzCg==",
                    "disposition": "filename.bin",
                },
            ]
            ```

    Raises:
        AttachmentOversizeException: If an attachment is larger than
            `MAIL_MAX_ATTACHMENT_SIZE`.

    !!! note
        Attachment files are inline, added as Base64 encoded strings.
        The encoded string will be part of the payload, sent over network to
        Celery.
    """
    if attachments is None:
        attachments = []
    for attachment in attachments:
        if len(attachment["base64"]) > current_app.config["MAIL_MAX_ATTACHMENT_SIZE"]:
            raise AttachmentOversizeException

    return _send_email_with_attachments.delay(data, attachments)


@shared_task(bind=True)
def send_email(self, data):
    """Celery task for sending emails.

    !!! warning
        Attachments do not work with Celery tasks since
        `flask_mail.Attachment` is not serializable in `JSON`
        nor `msgpack`. Note that a
        [custom serializer](https://docs.celeryq.dev/en/latest/userguide/calling.html#serializers)
        can be created if attachments are really needed.

        Use [`send_email_with_attachments`][invenio_mail.tasks.send_email_with_attachments]
        instead, which adds attachments by putting them into a base64 encoded
        string. This is not an optimal solution, it might get problematic if
        they are too large to handle by the messaging queue, so check for a
        maximum size beforehand.
    """
    msg = Message()
    msg.__dict__.update(data)

    _send(msg, self, original={"data": data})


@shared_task(bind=True)
def _send_email_with_attachments(self, data, attachments=None):
    """Celery task for sending emails with attachments."""
    if attachments is None:
        attachments = []
    msg = Message()
    msg.__dict__.update(data)

    for attachment in attachments:
        rawdata = b64decode(attachment.get("base64"))
        content_type = "application/octet-stream"
        if "content_type" in attachment:
            content_type = attachment.get("content_type")
        disposition = None
        if "disposition" in attachment:
            disposition = attachment.get("disposition")
        filename = None
        if "filename" in attachment:
            filename = attachment.get("filename")
        msg.attach(
            filename=filename,
            content_type=content_type,
            data=rawdata,
            disposition=disposition,
        )

    _send(msg, self, original={"data": data, "attachments": attachments})


def _send(msg, task, original):
    """Send emails and add exception handling."""
    try:
        current_app.extensions["mail"].send(msg)
    except (
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPHeloError,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPDataError,
        smtplib.SMTPNotSupportedError,
        Exception,
    ):
        if task.request.retries <= current_app.config["MAIL_MAX_RETRIES"]:
            raise task.retry(
                countdown=int(random.uniform(2, 4) ** task.request.retries)
            )
        else:
            logger = logging.getLogger("invenio-mail")
            # We log the original data as JSON, so that we can recover both the body and
            # attachments (in base64)
            logger.warning(json.dumps(original))
