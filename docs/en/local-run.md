# Running tests locally

Tests call an **external** Memes API over HTTP. You need a live `BASE_URL` and credentials.

**Language:** [Русский](../ru/local-run.md) · English

Quick path: [`quick-start.md`](quick-start.md).  
CI: [`ci-cd.md`](ci-cd.md). Pre-commit: [`pre-commit.md`](pre-commit.md).

---

## Run model

```text
Config (.env)
        │
        ▼
   Pytest (+ conftest fixtures)
        │
        ▼
   Endpoint classes
        │
        ▼
   HTTP → Memes API
        │
        ▼
   Asserts + Allure (steps, request/response)
```

| Layer | Role |
|------|------|
| `tests/` | scenarios |
| `conftest.py` | token, clients, `meme_fixture` |
| `endpoints/` | HTTP and checks |
| `utils/` | data and cases |
| `pytest.ini` | markers, `pythonpath`, Allure dir |

Markers: `critical` (smoke), `medium` (validation), `security` (auth/ownership).

More on the code: [`architecture.md`](architecture.md).

---

## Setup

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Unix:     source .venv/bin/activate

pip install -r requirements.txt
# for mypy / pre-commit:
make install-dev
# or: pip install -r requirements-dev.txt && pre-commit install
```

```bash
# Windows
copy .env.example .env
# Unix
cp .env.example .env
```

| Variable | Purpose |
|------------|------------|
| `BASE_URL` | API base URL |
| `TEST_USERNAME` | name for `POST /authorize` |
| `TEST_TOKEN` | saved token (reused if still valid) |

`.env` is not committed. Allure HTML needs the Allure CLI (`make allure`).

---

## What happens on `make test` / `pytest`

1. Pytest reads `pytest.ini` (`tests/`, `pythonpath=.`, `--alluredir=./allure-results`, `--clean-alluredir`).
2. Session fixture `auth_token`: live `TEST_TOKEN` or a new authorize.
3. Endpoint clients receive the token.
4. `meme_fixture` creates a meme when needed and deletes it in teardown (unless `skip_cleanup`).
5. Call → `_make_request` → HTTP + Allure attachments → `check_*`.

---

## Make commands (canonical)

| Command | What it does |
|---------|------------|
| `make install` | `pip install -r requirements.txt` |
| `make install-dev` | runtime + mypy/pre-commit + git hooks |
| `make lint` / `make mypy` | static type check (mypy) |
| `make pre-commit` | all pre-commit hooks on all files |
| `make pre-commit-run` | alias for `pre-commit` |
| `make pre-commit-install` | install git hooks only |
| `make test` | full suite |
| `make critical` | `@pytest.mark.critical` |
| `make medium` | `@pytest.mark.medium` |
| `make security` | `@pytest.mark.security` |
| `make authorize` / `get` / `post` / `put` / `delete` / `e2e` | a single test file |
| `make marker M=security` | arbitrary marker |
| `make file F=tests/test_memes_get.py` | arbitrary file |
| `make failed` | failed only (`--lf`) |
| `make last` | stop on first failure (`-x`) |
| `make allure` | generate and open HTML report |
| `make allure-gen` | generate only |
| `make clean` | caches and report artifacts |

Without Make:

```bash
python -m pytest
python -m pytest -m critical
python -m pytest tests/test_memes_post.py
python -m mypy
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## From command to report

```text
activate venv → .env → make test / pytest
                         → allure-results/
                         → make allure → browser
```

Failures: [`test-analysis.md`](test-analysis.md), [`troubleshooting.md`](troubleshooting.md).
