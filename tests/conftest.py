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


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import sys

import pytest
from flask import Blueprint, Flask
from flask_celeryext import FlaskCeleryExt


from invenio_mail import InvenioMail

PY3 = sys.version_info[0] == 3
if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


@pytest.fixture(scope='session')
def email_task_app(request):
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite://'
        ),
        CELERY_ALWAYS_EAGER=True,
        CELERY_RESULT_BACKEND="cache",
        CELERY_CACHE_BACKEND="memory",
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        MAIL_SUPPRESS_SEND=True
    )
    FlaskCeleryExt(app)

    InvenioMail(app, StringIO())

    return app


@pytest.fixture(scope='session')
def email_api_app(email_task_app):
    """Flask application fixture."""
    email_task_app.register_blueprint(
        Blueprint('invenio_mail', __name__, template_folder='templates')
    )

    return email_task_app
