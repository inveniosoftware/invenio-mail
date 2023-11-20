# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2023      University of Münster.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Background tasks for mail module."""
from __future__ import absolute_import, print_function

from base64 import b64decode

from celery import shared_task
from flask import current_app
from flask_mail import Message

from .errors import AttachmentOversizeException


def send_email_with_attachments(data, attachments):
    """Celery task for sending mails with attachments."""
    for attachment in attachments["attachments"]:
        if len(attachment["base64"]) > current_app.config["MAX_ATTACHMENT_SIZE"]:
            raise AttachmentOversizeException

    return _send_email_with_attachments.apply_async(
        kwargs={"data": data, "attachments": attachments}
    )


@shared_task
def send_email(data):
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

    current_app.extensions["mail"].send(msg)


@shared_task
def _send_email_with_attachments(data, attachments):
    msg = Message()
    msg.__dict__.update(data)

    if attachments is not None:
        for attachment in attachments["attachments"]:
            rawdata = b64decode(attachment.get("base64"))
            content_type = "application/octet-stream"
            if "content_type" in attachment:
                content_type = attachment.get("content_type")
            disposition = None
            if "disposition" in attachment:
                disposition = attachment.get("disposition")
            msg.attach(content_type=content_type, data=rawdata, disposition=disposition)

    current_app.extensions["mail"].send(msg)
