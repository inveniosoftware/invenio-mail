# SPDX-FileCopyrightText: 2015-2025 CERN.
# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: MIT

"""Invenio mail module.

The Invenio-Mail module is a tiny wrapper around Flask-Mail that provides
printing of emails to standard output when the configuration variable
`MAIL_SUPPRESS_SEND` is `True`.

Invenio-Mail also takes care of initializing Flask-Mail if not already
initialized.

First, initialize the extension:

```pycon
>>> from flask import Flask
>>> from invenio_mail import InvenioMail
>>> app = Flask('myapp')
>>> app.config.update(MAIL_SUPPRESS_SEND=True)
>>> InvenioMail(app)
<invenio_mail.ext.InvenioMail ...>

```

Next, let's send an email:

```pycon
>>> from flask_mail import Message
>>> msg = Message('Hello', sender='from@example.org',
...    recipients=['to@example.com'], body='Hello, World!')
>>> with app.app_context():
...     app.extensions['mail'].send(msg)
Content-Type: text/plain; charset="utf-8"...

```

## Template based messages

A simple API lets you create a message from a template, so you just have to
give the right arguments to get the full message. Moreover, it can create
a complete e-mail with both HTML and text content.

First, you need to instantiate the
[`TemplatedMessage`][invenio_mail.api.TemplatedMessage] class, just like you
would do with a standard `flask_mail.Message`:

```pycon
>>> from invenio_mail.api import TemplatedMessage
>>> with app.app_context():
...    msg = TemplatedMessage(
...         template_html='', # path to your template
...         template_body='', # path to your template
...         subject='Hello',
...         sender='from@example.org',
...         recipients=['to@example.com'],
...         ctx={
...             'content': 'Hello, World!',
...             'logo': 'logo.png',
...             'sender': 'Sender',
...             'user': 'User',
...         })

```

You just need to add the templates to use and a `ctx` dictionary,
containing the values useful to fill the templates. If you ommit these three
arguments, you will have the same result as you would with the standard
`flask_mail.Message` class.

Note that you must be in the application context in order to be able to render
the templates. Once you have created a message, you can send it the standard
way:

```pycon
>>> with app.app_context():
...     app.extensions['mail'].send(msg)
Content-Type: text/plain; charset="utf-8"...

```

## Writing extensions

By default you should just depend on Flask-Mail if you are writing an
extension which needs email sending functionality:

```python
from flask import current_app
from flask_mail import Message

def mystuff():
    msg = Message('Hello', sender='from@example.org',
                  recipients=['to@example.com'], body='Hello, World!')
    current_app.extensions['mail'].send(msg)
```

Remember to add Flask-Mail to the dependencies in your `pyproject.toml` file
as well:

```toml
[project]
dependencies = [
    "Flask-Mail>=0.9.1",
]
```
"""

from .ext import InvenioMail

__version__ = "2.3.2"

__all__ = ("InvenioMail", "__version__")
