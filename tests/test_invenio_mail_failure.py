# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2024      University of Münster.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module retry and failure tests."""

import smtplib
from unittest import mock

from celery.exceptions import Retry
from pytest import raises

from invenio_mail.tasks import _send_email_with_attachments, send_email


def test_send_email(email_task_failure_app, email_message):
    """Test if send_email is retried on failure."""
    with email_task_failure_app.app_context():
        mailer = email_task_failure_app.extensions["mail"]
        mailer.send = mock.Mock()
        mailer.send.side_effect = smtplib.SMTPHeloError(100, "Couldn't say helo!")
        with raises(Retry):
            send_email(email_message)


def test_send_email_with_attachments(email_task_failure_app, email_message):
    """Test if send_email is retried on failure."""
    with email_task_failure_app.app_context():
        mailer = email_task_failure_app.extensions["mail"]
        mailer.send = mock.Mock()
        mailer.send.side_effect = smtplib.SMTPHeloError(100, "Couldn't say helo!")
        with raises(Retry):
            _send_email_with_attachments(email_message)
