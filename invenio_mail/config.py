# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration for Invenio-Mail.

Invenio-Mail is a tiny integration layer between Invenio and Flask-Mail, so
please refer to
`Flask-Mail <https://pythonhosted.org/Flask-Mail/#configuring-flask-mail>`_'s
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
