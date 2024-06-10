..
    This file is part of Invenio.
    Copyright (C) 2015-2018 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 1.0.4 (released 2024-06-10)

- Added Github workflows for pypi publishing

Version 1.0.3 (released 2024-06-10)

- Pin Flask-Mail due to breaking changes

Version 1.0.2 (released 2018-12-05)

- Fixes issue with passing None context value to the e-mail template


Version 1.0.1 (released 2018-04-12)

- Fixes issue with task running in request context, when only the app context
  is needed. This causes issues when e.g host header injection protection is
  turned on.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
