# Pre-commit

Локальный quality gate **до** коммита. В CI mypy дополнительно гоняется в GitHub Actions ([`ci-cd.md`](ci-cd.md)).

**Язык:** Русский · [English](../en/pre-commit.md)

Конфиг: [`../../.pre-commit-config.yaml`](../../.pre-commit-config.yaml).  
Тот же mypy: [`../../pyproject.toml`](../../pyproject.toml).

---

## Установка

```bash
make install-dev
# или:
pip install -r requirements-dev.txt
pre-commit install
```

Только хуки (если deps уже стоят):

```bash
make pre-commit-install
```

---

## Запуск вручную

```bash
make pre-commit
# то же:
make pre-commit-run
# или:
pre-commit run --all-files
```

После `pre-commit install` хуки выполняются на каждый `git commit` для staged-файлов (mypy в конфиге с `pass_filenames: false` — полный прогон по `pyproject.toml`).

---

## Что проверяют хуки

| Hook | Зачем |
|------|--------|
| `trailing-whitespace` | хвостовые пробелы |
| `end-of-file-fixer` | перевод строки в конце файла |
| `check-yaml` | синтаксис YAML |
| `check-added-large-files` | случайно не закоммитить огромный файл |
| `check-merge-conflict` | маркеры конфликта |
| `debug-statements` | `pdb` / `print` breakpoint leftovers |
| `mypy` | типы (`endpoints`, `utils`, `conftest`) + `types-requests` |

---

## Если хук упал

1. Прочитать вывод (часто mypy указывает файл и код ошибки).
2. Исправить → снова `make pre-commit`.
3. Для типов локально удобно: `make lint`.

См. также [`troubleshooting.md`](troubleshooting.md).
