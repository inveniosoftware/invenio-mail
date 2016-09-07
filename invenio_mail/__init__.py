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

"""Invenio mail module.

The Invenio-Mail module is a tiny wrapper around Flask-Mail that provides
printing of emails to standard output when the configuration variable
``MAIL_SUPPRESS_SEND`` is true.

Invenio-Mail also takes care of initializing Flask-Mail if not already
initialized.


First, initialize the extension:

>>> from flask import Flask
>>> from invenio_mail import InvenioMail
>>> app = Flask('myapp')
>>> app.config.update(MAIL_SUPPRESS_SEND=True)
>>> InvenioMail(app)
<invenio_mail.ext.InvenioMail ...>


Next, let's send an email:

>>> from flask_mail import Message
>>> msg = Message("Hello", sender='from@example.org',
...    recipients=["to@example.com"], body='Hello, World!')
>>> with app.app_context():
...     app.extensions['mail'].send(msg)
Content-Type: text/plain; charset="utf-8"...


Using the API
-------------

A nice API let you create a message from a template, so you just have to
give the rights arguments to get the full message. Moreover, it creates
a complete e-mail with HTML message and text only message.

To do so, you need to instantiate
a :class:`~invenio_mail.api.TemplatedMessage` object, just like you
would with a standard :class:`flask_mail.Message`:


When you have initialized your extension, you can create an email:

>>> from invenio_mail.api import TemplatedMessage
>>> with app.app_context():
...    msg = TemplatedMessage(
...         template_html="", # path to your template
...         template_body="", # path to your template
...         subject="Hello",
...         sender='from@example.org',
...         recipients=["to@example.com"],
...         ctx={
...             "content": "Hello, World!",
...             "logo": "logo.png",
...             "sender": "Sender",
...             "user": "User"
...         })

You just need to add the templates to use and a ``ctx`` dictionnary,
containing the values useful to fill the templates.

If you ommit these 3 arguments, you will have the same result as you would
with the standard :class:`flask_mail.Message` class.

Note that you must be in the context of the application in order to
be able to render the templates.

Once you have created a message, you can send it the standard way:

>>> with app.app_context():
...     app.extensions['mail'].send(msg)
Content-Type: text/plain; charset="utf-8"...


Writing extensions
------------------
By default you should just depend on Flask-Mail if you are writing an
extension which needs email sending functionality:

.. code-block:: python

   from flask import current_app
   from flask_mail import Message

   def mystuff():
       msg = Message("Hello", sender='from@example.org',
                     recipients=["to@example.com"], body='Hello, World!')
       current_app.extensions['mail'].send(msg)


Remember to add Flask-Mail to your ``setup.py`` file as well:

.. code-block:: python

   setup(
       # ...
       install_requires = ['Flask-Mail>=0.9.1',]
       #...
    )
"""

from __future__ import absolute_import, print_function

from .ext import InvenioMail
from .version import __version__

__all__ = ('__version__', 'InvenioMail')
