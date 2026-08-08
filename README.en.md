# 🧪 Memes API — Test Automation

**Language:** [Русский](README.md) · English

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.1-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.15.2-purple?logo=allure&logoColor=white)](https://allurereport.org/)
[![CI](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-GitHub%20Pages-orange?logo=allure&logoColor=white)](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aliaksandr--stanavy-181717?logo=github&logoColor=white)](https://github.com/aliaksandr-stanavy)

**API test automation framework** for Memes API built with Python + Pytest + Allure + Requests.

> This project is a **demonstration of an industrial approach** to API testing: clean architecture, deep security checks, automated reporting, and a full CI/CD pipeline.

| Start | Documentation |
|-------|-----------------|
| [Quick start](docs/en/quick-start.md) (~5 min) | [EN index](docs/en/index.md) · [RU](docs/ru/index.md) · [languages](docs/README.md) |

---

## 📖 About

The framework shows how to build API automation infrastructure focused on **reliability, maintainability, and transparent results**.

**Key features:**
- 🏗️ **API Page Object** — clear client architecture.
- 📊 **Allure reports** — with steps, request/response attachments, and token masking.
- 🏷️ **Priority markers** (`critical` / `medium` / `security`) for flexible runs.
- 🔒 **Security scenarios** — `401`/`403` checks with confirmation that data **did not change**.
- ⚙️ **CI/CD** — GitHub Actions with automatic report publishing to GitHub Pages.
- 🎲 **Data generation** (Faker) and **polling** (Tenacity) for wait-based tests.
- 🛡️ **Static analysis** — mypy + TypedDict, pre-commit hooks in CI.

### 🔥 What this demonstrates

- **Resource isolation:** session token, disposable kill-token, and guaranteed meme teardown (even when a test fails).
- **Security beyond status codes:** we verify not only `401`/`403`, but that the resource **really did not change**.
- **Known API defect:** captured with `xfail` (PUT returns `id` as a string).
- **Code quality:** typed clients and payloads (mypy + TypedDict), pre-commit in CI.
- **Full reporting loop:** Allure → GitHub Actions → GitHub Pages.

---

## 🛠 Stack

| Component | Technology |
|-----------|------------|
| 🐍 Language | Python 3.12+ |
| 🧪 Test runner | Pytest 9.0.1 |
| 🌐 HTTP client | Requests 2.32.4 |
| 📊 Reporting | allure-pytest 2.15.2 |
| 🎲 Data generation | Faker 38.2.0 |
| 🔁 Retry / polling | Tenacity 9.1.2 |
| 🛡️ Types / hooks | mypy, TypedDict, pre-commit |
| ⚙️ CI/CD | GitHub Actions → Allure on Pages |
| 🔗 Target API | Memes API (set URL in `.env` / Secrets as `BASE_URL`) |

---

## 🚀 Quick start

```bash
git clone https://github.com/aliaksandr-stanavy/api-test-automation-framework.git
cd api-test-automation-framework

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # or: cp .env.example .env
# set BASE_URL, TEST_USERNAME, TEST_TOKEN (optional)

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

## 📁 Layout

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

---

## 📚 Documentation

Canonical index: **[docs/en/index.md](docs/en/index.md)**. Navigation by task below.

### Documentation map

| If you need to... | Document | ⏱ Approx. time |
|---|---|---|
| **Run the tests** | [Quick start](docs/en/quick-start.md) | ~5 minutes |
| **Understand the code** | [Architecture](docs/en/architecture.md) | 15 minutes |
| **Pick a fixture** | [Fixtures reference](docs/en/fixtures-reference.md) | 10 minutes |
| **Learn the product contract** | [BRD](docs/en/brd.md) | 10 minutes |
| **Check expected status codes** | [QA requirements](docs/en/qa-requirements.md) | 10 minutes |
| **See all Make targets** | [Local run](docs/en/local-run.md) | 5 minutes |
| **Debug a red CI** | [CI/CD](docs/en/ci-cd.md) + [Test analysis](docs/en/test-analysis.md) | 15 minutes |
| **Fix a problem** | [Troubleshooting](docs/en/troubleshooting.md) | 5 minutes |

Changelog: [CHANGELOG.md](CHANGELOG.md).

---

## ✅ Coverage

- Authorize, meme CRUD, E2E lifecycle  
- Field validation and invalid ids  
- Security: `401` without/with bad token; `403` for non-owner plus a check that the resource is unchanged  
- Known bug: PUT `id` as `string` — `xfail` (see [qa-requirements](docs/en/qa-requirements.md))

Tests are integration tests: the API must be reachable. Allure in `_make_request` attaches request/response (`Authorization` is masked). The kill-token test uses a disposable token — session `auth_token` is never killed.

---

## 📊 Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
# or: make allure
```

In CI the report is published to **GitHub Pages**:
[https://aliaksandr-stanavy.github.io/api-test-automation-framework/](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
Details: [local-run](docs/en/local-run.md), [ci-cd](docs/en/ci-cd.md).

---

## 👤 Author

This project was built while developing my expertise in **Full Stack QA** and is part of my public **GitHub portfolio**.
Its goal is to show modern approaches to API frameworks, test organization, and CI/CD.

Feedback, suggestions, and professional conversation are welcome.

- 🌐 **GitHub Portfolio:** https://github.com/aliaksandr-stanavy
- 💼 **LinkedIn:** https://www.linkedin.com/in/aliaksandr-stanavy/
- 📧 **Email:** aliaksandr.stanavy@gmail.com

---

## 📄 License

This project is distributed under the **MIT** license.

See [LICENSE](LICENSE) for details.

© 2026 Aliaksandr Stanavy
