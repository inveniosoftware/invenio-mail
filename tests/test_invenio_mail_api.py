# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

from datetime import datetime

from flask import Flask, render_template

from invenio_mail.api import TemplatedMessage


def _get_params():
    return {
        "subject": "subject",
        "recipients": ["recipient@inveniosoftware.com"],
        "sender": "sender@inveniosoftware.com",
        "cc": "cc@inveniosoftware.com",
        "bcc": "bcc@inveniosoftware.com",
        "reply_to": "reply_to@inveniosoftware.com",
        "date": datetime.now(),
        "attachments": [],
        "charset": None,
        "extra_headers": None,
        "mail_options": [],
        "rcpt_options": []
    }


def _get_context():
    return {
        "user": "User",
        "content": "This a a content",
        "sender": "sender"
    }


def test_init(email_api_app):
    """Test the constructor."""
    # we test that all the fields given are inside the message
    params = _get_params()
    ctx = _get_context()

    with email_api_app.app_context():
        msg = TemplatedMessage("invenio_mail/base.txt",
                               "invenio_mail/base.html",
                               ctx,
                               **params)
    assert msg.subject == params["subject"]
    assert msg.recipients == params["recipients"]
    assert msg.sender == params["sender"]
    assert msg.cc == params["cc"]
    assert msg.bcc == params["bcc"]
    assert msg.reply_to == params["reply_to"]
    assert msg.date == params["date"]

    # let's check that the body and html are correctly formatted
    assert "<p>Dear {0},</p>".format(ctx["user"]) in msg.html
    assert "Dear {0},".format(ctx["user"]) in msg.body
    assert "<p>{0}</p>".format(ctx["content"]) in msg.html
    assert "{0}".format(ctx["content"]) in msg.body
    assert ctx["sender"] in msg.html
    assert ctx["sender"] in msg.body
