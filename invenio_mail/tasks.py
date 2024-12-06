# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2023      University of Münster.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Background tasks for mail module."""

import smtplib
from base64 import b64decode

from celery import Task, shared_task
from flask import current_app
from flask_mail import Message

from .errors import AttachmentOversizeException


class LoggingTask(Task):
    """Task implementation to add logging functionality if task finally fails."""

    max_retries = 2

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """When sending the message fails report to Logs."""
        current_app.logger.error("Mail could not be dispatched!")
        if current_app.config["MAIL_LOG_FAILED_MESSAGES"]:
            current_app.logger.info(kwargs["data"]["body"])
            if "attachments" in kwargs:
                current_app.logger.info(kwargs["attachments"])


def send_email_with_attachments(data, attachments=None):
    """Celery task for sending mails with attachments.

    :param data: a dict with the email fields
    :param attachments: a list of dicts, in the following form:
        attachments = [
                {
                    "base64": "RGllcyBpc3QgZGFzIEhhdXMgdm9tIE5pa29sYXVzCg==",
                    "disposition": "filename.bin",
                },
            ]

    Note: attachment files are inline, added as Base64 encoded strings.
    The encoded string will be part of the payload, sent over network to Celery.
    """
    if attachments is None:
        attachments = []
    for attachment in attachments:
        if len(attachment["base64"]) > current_app.config["MAIL_MAX_ATTACHMENT_SIZE"]:
            raise AttachmentOversizeException

    return _send_email_with_attachments.delay(data, attachments)


@shared_task(bind=True, base=LoggingTask)
def send_email(self, data):
    """Celery task for sending emails.

    .. warning::

       Attachments do not work with Celery tasks since
       :class:`flask_mail.Attachment` is not serializable in ``JSON``
       nor ``msgpack``. Note that a
       `custom serializer <http://docs.celeryproject.org/en/latest/
       userguide/calling.html#serializers>`__
       can be created if attachments are really needed.

       This version adds attachments by putting them into a base64 encoded string.
       This is not an optimal solution, it might get problematic if they are too
       large to handle by the messaging queue, so check for a maximum size beforehand.
    """
    msg = Message()
    msg.__dict__.update(data)

    _send(msg, self)


@shared_task(bind=True, base=LoggingTask)
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
        msg.attach(content_type=content_type, data=rawdata, disposition=disposition)

    _send(msg, self)


def _send(msg, task):
    """Send emails and add exception handling."""
    try:
        current_app.extensions["mail"].send(msg)
    except (
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPHeloError,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPDataError,
        smtplib.SMTPNotSupportedError,
    ):
        if task.request.retries <= 2:
            raise task.retry(countdown=current_app.config["MAIL_RETRY_COUNTDOWN"])
