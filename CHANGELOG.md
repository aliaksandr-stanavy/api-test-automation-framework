# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-06

### Added
- Initial release of API test automation framework for Memes API
- Page Object–style endpoint layer (`endpoints/`) with shared `Endpoint` base class
- Pytest fixtures (`conftest.py`): session `auth_token`, CRUD clients, `meme_fixture`, `as_client`, `other_user_token`, shared PUT-negative meme
- Parametrized scenarios: Authorize, meme CRUD, E2E lifecycle, positive/negative/contract checks
- Security: `401` without/with invalid token; ownership `403` for non-owner PUT/DELETE, with post-checks that the resource is unchanged
- Pytest markers: `critical`, `medium`, `security`
- Allure reporting with steps and request/response attachments (`Authorization` masked)
- CI/CD via GitHub Actions (mypy → pytest → Allure on GitHub Pages); Pages deploy on `push` to `main`/`master` only
- `Makefile` for local runs; mypy + TypedDict; pre-commit hooks
- Bilingual documentation: `docs/ru/` and `docs/en/` (architecture, fixtures, BRD, QA requirements, local run, CI/CD, troubleshooting)
- Known API defect documented: PUT `/meme/<id>` returns `id` as `string` (`xfail`)

### Technologies
- Python 3.12+
- Pytest 9.0.1
- Requests 2.32.4
- allure-pytest 2.15.2
- Tenacity 9.1.2
- Faker 38.2.0
- python-dotenv 1.2.1
- GitHub Actions
