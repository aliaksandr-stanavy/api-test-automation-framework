# Pre-commit

Local quality gate **before** commit. In CI, mypy also runs in GitHub Actions ([`ci-cd.md`](ci-cd.md)).

**Language:** [Русский](../ru/pre-commit.md) · English

Config: [`../../.pre-commit-config.yaml`](../../.pre-commit-config.yaml).  
Same mypy: [`../../pyproject.toml`](../../pyproject.toml).

---

## Install

```bash
make install-dev
# or:
pip install -r requirements-dev.txt
pre-commit install
```

Hooks only (if deps are already installed):

```bash
make pre-commit-install
```

---

## Run manually

```bash
make pre-commit
# same:
make pre-commit-run
# or:
pre-commit run --all-files
```

After `pre-commit install`, hooks run on every `git commit` for staged files (mypy in the config uses `pass_filenames: false` — full run per `pyproject.toml`).

---

## What the hooks check

| Hook | Why |
|------|--------|
| `trailing-whitespace` | trailing spaces |
| `end-of-file-fixer` | newline at end of file |
| `check-yaml` | YAML syntax |
| `check-added-large-files` | avoid accidentally committing a huge file |
| `check-merge-conflict` | conflict markers |
| `debug-statements` | `pdb` / `print` breakpoint leftovers |
| `mypy` | types (`endpoints`, `utils`, `conftest`) + `types-requests` |

---

## If a hook fails

1. Read the output (mypy often points to the file and error code).
2. Fix → run `make pre-commit` again.
3. For types locally, `make lint` is convenient.

See also [`troubleshooting.md`](troubleshooting.md).
