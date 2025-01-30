# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2024 University of Münster.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Logging handler for mail module."""

import logging

from flask import current_app


class InvenioMailLogging(object):
    """Invenio-mail specific logging handler to allow logging of mail contents."""

    def __init__(self):
        """Initialize the Invenio-mail logger."""
        self._logger = logging.getLogger("invenio-mail-logging")
        self.install_handler()

    def install_handler(self):
        """Install log handler."""
        handler = logging.StreamHandler()

        if current_app.config["MAIL_LOGGING_LEVEL"] is not None:
            level = current_app.config["MAIL_LOGGING_LEVEL"]
            self._logger.setLevel(level)
            handler.setLevel(level)
            self._logger.addHandler(handler)

    @property
    def logger(self):
        """Access to the mail-logger."""
        return self._logger
