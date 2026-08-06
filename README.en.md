# Memes API — Test Automation

**Language:** [Русский](README.md) · English

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.1-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.15.2-purple?logo=allure&logoColor=white)](https://allurereport.org/)
[![CI](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-GitHub%20Pages-orange?logo=allure&logoColor=white)](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aliaksandr--stanavy-181717?logo=github&logoColor=white)](https://github.com/aliaksandr-stanavy)

**API test automation framework** for Memes API built with Python + Pytest + Allure + Requests.

| Start | Documentation |
|-------|-----------------|
| [Quick start](docs/en/quick-start.md) (~5 min) | [EN index](docs/en/index.md) · [RU](docs/ru/index.md) · [languages](docs/README.md) |

---

## About

A demonstration framework for API test automation. It shows how to build a test infrastructure with:

- clear architecture (API Page Object);
- Allure reports with steps and request/response attachments;
- priority markers (`critical` / `medium` / `security`);
- positive, negative, and security/ownership scenarios;
- CI/CD via GitHub Actions and Allure on Pages;
- data generation (Faker) and kill-token polling (Tenacity);
- static checks (mypy + TypedDict) and pre-commit hooks.

### What this demonstrates

- resource isolation: session token, disposable kill-token, meme teardown even when a test fails;
- security beyond status codes: `401`/`403` plus checks that data is unchanged / the meme still exists;
- a known API defect captured with `xfail` (PUT returns `id` as a string);
- typed clients and payloads (mypy + TypedDict) and pre-commit in CI;
- full reporting loop: Allure (request/response, token masking) → GitHub Actions → Pages.

---

## Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Test runner | Pytest 9.0.1 |
| HTTP client | Requests 2.32.4 |
| Reporting | allure-pytest 2.15.2 |
| Data generation | Faker 38.2.0 |
| Retry / polling | Tenacity 9.1.2 |
| Types / hooks | mypy, TypedDict, pre-commit |
| CI/CD | GitHub Actions → Allure on Pages |
| Target API | Memes API (set URL in `.env` / Secrets as `BASE_URL`) |

---

## Quick start

```bash
git clone https://github.com/aliaksandr-stanavy/api-test-automation-framework.git
cd api-test-automation-framework

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # or: cp .env.example .env
# set BASE_URL, TEST_USERNAME, TEST_TOKEN

make critical
# or: pytest -m critical -q
```

| Variable | Description |
|----------|-------------|
| `BASE_URL` | Memes API base URL |
| `TEST_USERNAME` | name for `POST /authorize` |
| `TEST_TOKEN` | saved token (reused while still valid) |

CI uses **GitHub Secrets**. Full guide: [quick-start](docs/en/quick-start.md) · Make & Allure: [local-run](docs/en/local-run.md).

---

## Layout

```text
api-test-automation-framework/
├── endpoints/           # API clients + shared asserts
├── tests/               # scenarios
├── utils/               # generators, cases, TypedDict
├── conftest.py          # fixtures
├── Makefile
├── docs/
│   ├── README.md        # language switcher
│   ├── ru/              # documentation (RU)
│   └── en/              # documentation (EN)
├── .github/workflows/   # CI/CD
├── LICENSE
└── CHANGELOG.md
```

Code and fixtures: [architecture](docs/en/architecture.md) · [fixtures-reference](docs/en/fixtures-reference.md).

---

## Documentation

Canonical index: **[docs/en/index.md](docs/en/index.md)**. Same reading order and task map below.

### Reading order

1. [Quick start](docs/en/quick-start.md) — green run in ~5 minutes  
2. [Architecture](docs/en/architecture.md) — how the code is structured  
3. [Fixtures reference](docs/en/fixtures-reference.md) — which fixture to use  
4. [BRD](docs/en/brd.md) — *what* the API does  
5. [QA requirements](docs/en/qa-requirements.md) — *how* we test  
6. [Local run](docs/en/local-run.md) — Make, pytest, Allure  
7. [Pre-commit](docs/en/pre-commit.md) — hooks before commit  
8. [CI/CD](docs/en/ci-cd.md) — GitHub Actions  
9. [Test analysis](docs/en/test-analysis.md) — reading failures  
10. [Troubleshooting](docs/en/troubleshooting.md) — common issues  

Changelog: [CHANGELOG.md](CHANGELOG.md).

### By task

| Need | Document |
|------|----------|
| Run tests now | [quick-start](docs/en/quick-start.md) |
| Understand the framework | [architecture](docs/en/architecture.md) |
| Pick a fixture | [fixtures-reference](docs/en/fixtures-reference.md) |
| Product contract | [brd](docs/en/brd.md) |
| Expected codes & markers | [qa-requirements](docs/en/qa-requirements.md) |
| All Make targets | [local-run](docs/en/local-run.md) |
| Debug red CI | [ci-cd](docs/en/ci-cd.md) + [test-analysis](docs/en/test-analysis.md) |
| “It doesn’t work” | [troubleshooting](docs/en/troubleshooting.md) |

---

## Coverage

- Authorize, meme CRUD, E2E lifecycle  
- Field validation and invalid ids  
- Security: `401` without/with bad token; `403` for non-owner plus a check that the resource is unchanged  
- Known bug: PUT `id` as `string` — `xfail` (see [qa-requirements](docs/en/qa-requirements.md))

Tests are integration tests: the API must be reachable. Allure in `_make_request` attaches request/response (`Authorization` is masked). The kill-token test uses a disposable token — session `auth_token` is never killed.

---

## Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
# or: make allure
```

In CI the report is published to **GitHub Pages**:
[https://aliaksandr-stanavy.github.io/api-test-automation-framework/](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
(the link becomes live after the first successful deploy on `main`). Details: [local-run](docs/en/local-run.md), [ci-cd](docs/en/ci-cd.md).

---

## Author and license

Built while developing expertise in **Full Stack QA | Automation QA**.

- GitHub: [aliaksandr-stanavy](https://github.com/aliaksandr-stanavy)
- LinkedIn: [aliaksandr-stanavy](https://www.linkedin.com/in/aliaksandr-stanavy/)
- License: [MIT](LICENSE) © 2026 Aliaksandr Stanavy
