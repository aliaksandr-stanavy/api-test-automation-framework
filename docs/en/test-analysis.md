# Test analysis

How to triage failures: locally and in CI.  
FAQ (“Allure won’t open / no .env”) → [`troubleshooting.md`](troubleshooting.md).  
Expected codes → [`qa-requirements.md`](qa-requirements.md).

**Language:** [Русский](../ru/test-analysis.md) · English

---

## Triage process (checklist)

### 1. Identify the test

- function name / parametrize id;
- marker: `critical` | `medium` | `security`;
- Allure title / feature / story.

### 2. Open the step in Allure

`_make_request` attaches to the step:

| Attachment | Contents |
|------------|----------|
| `request` | method, url, headers (`Authorization` → `***`) |
| `request_body` | JSON/text body (when present) |
| `response` | status_code, headers |
| `response_body` | JSON or raw text |
| `network_error` | if requests failed |

Compare actual status/body with the table in [`qa-requirements.md`](qa-requirements.md).

### 3. Separate known defects

| Signal | Meaning |
|--------|---------|
| `xfail` on `test_update_meme_response_id_is_int` | BUG-001: PUT returns `id` as `string` — **expected** |
| strict xfail became unexpected pass | stand bug is **fixed** — update tests/docs |

Do not mask BUG-001 with `str(actual) == str(expected)`.

### 4. Where to view the report

| Environment | How |
|-------------|-----|
| Local | after a run: `make allure` (Allure CLI required) |
| CI | GitHub Pages (**github-pages** environment) or artifact `allure-results-raw` |
| CI logs | Actions → job **Run API Tests** → pytest / mypy step |

Pipeline: [`ci-cd.md`](ci-cd.md).

### 5. Typical cause classification

| Observation | Where to look |
|-------------|----------------|
| Wrong status vs contract | `qa-requirements.md`, request/response body |
| `401` on CRUD | token / Secrets / killed the wrong token |
| `403` on PUT/DELETE | ownership (other user) — often expected |
| `404` | id missing or already deleted |
| Failure in fixture setup | create meme / authorize; check setup-step attach |
| mypy red, pytest never ran | `make lint`, [`pre-commit.md`](pre-commit.md) |

If the symptom is known — table in [`troubleshooting.md`](troubleshooting.md).

---

## Filtering for a recheck

```bash
make critical          # smoke
make security          # auth / ownership
make file F=tests/test_memes_update.py
pytest -k "forbidden" -q
make failed            # previously failed only
```

---

## Related docs

- [`architecture.md`](architecture.md) — where attach and asserts live in code  
- [`local-run.md`](local-run.md) — commands  
- [`ci-cd.md`](ci-cd.md) — jobs and Pages  
