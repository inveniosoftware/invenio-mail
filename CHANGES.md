<!--
SPDX-FileCopyrightText: 2015-2025 CERN.
SPDX-FileCopyrightText: 2026 TU Wien.
SPDX-FileCopyrightText: 2026 California Institute of Technology.
SPDX-License-Identifier: MIT
-->

# Changes

## Version v2.3.2 (released 2026-11-12)

- chore: apply ruff linter fixes
- fix(tests): replace import from `six` with `io`

## Version v2.3.1 (released 2026-07-16)

- chore(setup): migrate from setuptools to hatchling
- chore(licenses): update license headers to use SPDX
- tests: extend support to Python 3.14

## Version v2.3.0 (released 2025-03-27)

- tasks: enable optional logging of failed emails

## Version 2.2.1 (released 2025-01-29)

- add filename to attachments

## Version 2.2.0 (released 2024-12-20)

- retry e-mail sending on failure with random backoff

## Version 2.1.1 (released 2024-05-28)

- installation: upper pin flask-mail due to breaking changes in v0.10.0

## Version 2.1.0 (released 2023-11-29)

- add a func to send e-mails with inline attachments

## Version 2.0.0 (released 2023-10-06)

- config: introduce MAIL_DEFAULT_REPLY_TO
- global: clean test infrastructure
- global: bump minimal python version to 3.7
- global: migrate CI to gh-actions

## Version 1.0.2 (released 2018-12-05)

- Fixes issue with passing None context value to the e-mail template

## Version 1.0.1 (released 2018-04-12)

- Fixes issue with task running in request context, when only the app context
  is needed. This causes issues when e.g host header injection protection is
  turned on.

## Version 1.0.0 (released 2018-03-23)

- Initial public release.
