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
    msg.subject = data.get("subject")
    if "html" in data:
        msg.html = data.get("html")

    msg.body = data.get("body")
    msg.recipients = data.get("recipients")
    msg.sender = data.get("sender")
    if "reply_to" in data:
        msg.reply_to = data.get("reply_to")

    if "date" in data:
        msg.date = data.get("date")

    if "cc" in data:
        msg.cc = data.get("cc")

    if "bcc" in data:
        msg.cc = data.get("bcc")

    if "charset" in data:
        msg.cc = data.get("charset")

    if "extra_headers" in data:
        msg.cc = data.get("extra_headers")

    if "mail_options" in data:
        msg.cc = data.get("mail_options")

    if "rcpt_options" in data:
        msg.cc = data.get("rcpt_options")

    if "attachments" in data:
        for attachment in data.get("attachments"):
            rawdata = b64decode(attachment.get("base64"))
            content_type = "application/octet-stream"
            if "content_type" in attachment:
                content_type = attachment.get("content_type")
            disposition = None
            if "disposition" in attachment:
                disposition = attachment.get("disposition")
            msg.attach(content_type=content_type, data=rawdata, disposition=disposition)

    current_app.extensions["mail"].send(msg)
