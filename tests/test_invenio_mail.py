# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT

"""Module tests."""

import sys

from flask import Flask
from flask_mail import Message

from invenio_mail import InvenioMail

PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


def test_version():
    """Test version import."""
    from invenio_mail import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioMail(app)
    assert "invenio-mail" in app.extensions

    app = Flask("testapp")
    ext = InvenioMail()
    assert "invenio-mail" not in app.extensions
    ext.init_app(app)
    assert "invenio-mail" in app.extensions


def test_print_email():
    """Test printing of email."""
    app = Flask("testapp")
    app.config.update(MAIL_SUPPRESS_SEND=True)

    output = StringIO()
    InvenioMail(app, stream=output)

    with app.app_context():
        msg = Message(
            "Test subject",
            sender="from@example.com",
            recipients=["to@example.com"],
            body="Test Body",
        )
        app.extensions["mail"].send(msg)

    email = output.getvalue()
    output.close()

    sep = "\r\n" if PY3 else "\n"

    assert f"Subject: Test subject{sep}" in email
    assert f"From: from@example.com{sep}" in email
    assert f"To: to@example.com{sep}" in email
    assert f"{sep}{sep}Test Body" in email
