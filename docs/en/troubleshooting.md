# Troubleshooting

Common problems and quick fixes.  
How to **systematically** triage a failing test: [`test-analysis.md`](test-analysis.md).  
Setup and commands: [`local-run.md`](local-run.md), [`quick-start.md`](quick-start.md).

**Language:** [Русский](../ru/troubleshooting.md) · English

---

## Symptom → fix

| Symptom | Typical cause | Fix |
|---------|---------------|-----|
| `BASE_URL is not set` | missing `.env` or empty `BASE_URL` | copy `.env.example` → `.env` and fill in; in CI — Secrets |
| Network / timeout / connection | stand down, wrong URL | check `BASE_URL` in browser/curl |
| `401` on CRUD | dead, empty, or killed token | re-authorize; do not use the session token in kill tests |
| `403` on PUT/DELETE | caller is not the meme owner | expected for another user; own resource — `meme_fixture` |
| `404` on GET/DELETE | meme missing / already deleted | check id; repeat DELETE → `404` by contract |
| `400` on POST/PUT | body validation | match payload to [`qa-requirements.md`](qa-requirements.md); for PUT — existing id |
| `meme_fixture` fails on setup | create did not return int id | check Allure create attach; API availability |
| mypy / `make lint` red | types / incomplete defs | fix from output; `make pre-commit` |
| pre-commit red | hook (whitespace, mypy, …) | read hook output; [`pre-commit.md`](pre-commit.md) |
| Allure won’t open | no Allure CLI | `npm install -g allure-commandline` (or OS equivalent); then `make allure` |
| Empty / odd Allure | run without `--alluredir` or cleaned | run via project `pytest`/`make test` (`pytest.ini`) |
| CI red on mypy | same type errors | `make lint` locally before push ([`ci-cd.md`](ci-cd.md)) |
| CI red on pytest | test failure / stand / secrets | Actions → Run API Tests; report on Pages; [`test-analysis.md`](test-analysis.md) |
| CI “green” report but pytest step red | `continue-on-error: true` on pytest | check step summary and Allure, not only deploy |

---

## Quick environment checks

```bash
# is venv active and packages importable
python -c "import pytest, requests; print('ok')"

# is BASE_URL set (without printing secrets to chat/public logs)
python -c "from endpoints.constants import BASE_URL; print(bool(BASE_URL))"
```

---

## Where to go next

| Question | Document |
|----------|----------|
| How the framework is built | [`architecture.md`](architecture.md) |
| What the API should return | [`qa-requirements.md`](qa-requirements.md) |
| How the pipeline works | [`ci-cd.md`](ci-cd.md) |
| Table of contents | [`index.md`](index.md) |
