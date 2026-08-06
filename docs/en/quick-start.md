# Quick start

Goal: see a **green** run in a few minutes. Details: [`local-run.md`](local-run.md).

**Language:** [Русский](../ru/quick-start.md) · English

## 1. Prerequisites

- Python 3.12+
- access to Memes API (`BASE_URL`)
- Make (optional)

## 2. Setup

```bash
git clone https://github.com/aliaksandr-stanavy/api-test-automation-framework.git
cd api-test-automation-framework

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

```bash
# Windows
copy .env.example .env
# Linux/macOS
cp .env.example .env
```

Fill in `.env`: `BASE_URL`, `TEST_USERNAME`, `TEST_TOKEN`.
Template: [`.env.example`](../../.env.example) (`BASE_URL=https://api.example.com` — replace with your stand URL).

## 3. Fastest run

```bash
pytest -m critical -q
# or:
make critical
```

Expected: critical tests `passed` (one `xfail` on PUT `id` — known API bug, see [`qa-requirements.md`](qa-requirements.md)).

## 4. Minimal test example

Project style (Page Object + checks). You do not need to add this file to the suite — it is enough to see the pattern:

```python
from endpoints.authorize import Authorize


def test_authorize_smoke():
    auth = Authorize()
    auth.authorize("demo_user")
    auth.check_status_is_200()
    auth.check_response_is_json()
    assert auth.json.get("token"), "token missing"
```

Run a single file:

```bash
pytest path/to/your_smoke.py -q
```

### Expected outcomes

| Outcome | Meaning |
|---------|---------|
| Test green | API reachable, authorize returned a token |
| `BASE_URL is not set` | missing or empty `.env` → [`troubleshooting.md`](troubleshooting.md) |
| `401` / network | check URL and stand availability |

## 5. Useful commands

| Command | What it does |
|---------|--------------|
| `make test` | full suite |
| `make critical` | `@pytest.mark.critical` only |
| `make allure` | Allure HTML report |
| `make pre-commit` | all pre-commit hooks |

Full Make list: [`local-run.md`](local-run.md).

## Next

- How the code is structured → [`architecture.md`](architecture.md)
- Failures and FAQ → [`troubleshooting.md`](troubleshooting.md)
- Table of contents → [`index.md`](index.md)
