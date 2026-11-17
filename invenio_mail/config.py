# SPDX-FileCopyrightText: 2016-2025 CERN.
# SPDX-License-Identifier: MIT

"""Configuration for Invenio-Mail.

Invenio-Mail is a tiny integration layer between Invenio and Flask-Mail, so
please refer to
[Flask-Mail](https://flask-mail.readthedocs.io/en/latest/#configuring-flask-mail)'s
list of configuration variables.
"""

import logging

MAIL_DEFAULT_REPLY_TO = None
"""Reply to mail address for e-mails."""

MAIL_MAX_ATTACHMENT_SIZE = 1000000
"""Max size of inline attachments, in bytes."""

MAIL_MAX_RETRIES = 2
"""How often will we repeat if a problem occurred."""

MAIL_MIN_LOGGING_LEVEL = logging.ERROR
"""Minimum logging level for the mail logger."""
