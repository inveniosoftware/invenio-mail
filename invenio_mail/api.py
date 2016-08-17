# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
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

"""Templated message class for improved messages."""

from __future__ import absolute_import, print_function

from flask import render_template
from flask_mail import Message


class TemplatedMessage(Message):
    """Class for templated messages.

    You can give a template name and its arguments to automatically create
    the message you want to send.
    """

    def __init__(self, template_body=None, template_html=None, ctx=None,
                 **kwargs):
        """Constructor of TemplatedMessage class.

        You can give all the parameters available in the flask_mail.Message
        constructor: https://pythonhosted.org/Flask-Mail/#flask_mail.Message.

        However, if you provide templates, it will generate a text and html
        body that will erase the `html` and `body` parameters.

        Note that if the template_body is not given, the text will be
        extracted from the html thanks to html2text

        :param template_body: path to the text template
        :type template_body: str
        :param template_html: path to the html template
        :type template_html: str
        :param ctx: a dictionnary containing all the info needed to generate
            the temmplates.
        :type ctx: dict
        """
        if template_body:
            kwargs["body"] = render_template(template_body, **ctx)
        if template_html:
            kwargs["html"] = render_template(template_html, **ctx)
        super(TemplatedMessage, self).__init__(**kwargs)
