# Локальный запуск тестов

Тесты ходят во **внешний** Memes API по HTTP. Нужны живой `BASE_URL` и учётные данные.

**Язык:** Русский · [English](../en/local-run.md)

Быстрый путь: [`quick-start.md`](quick-start.md).  
CI: [`ci-cd.md`](ci-cd.md). Pre-commit: [`pre-commit.md`](pre-commit.md).

---

## Принцип прогона

```text
Конфиг (.env)
        │
        ▼
   Pytest (+ фикстуры conftest)
        │
        ▼
   Endpoint-классы
        │
        ▼
   HTTP → Memes API
        │
        ▼
   Ассерты + Allure (шаги, request/response)
```

| Слой | Роль |
|------|------|
| `tests/` | сценарии |
| `conftest.py` | токен, клиенты, `meme_fixture` |
| `endpoints/` | HTTP и checks |
| `utils/` | данные и cases |
| `pytest.ini` | маркеры, `pythonpath`, Allure dir |

Маркеры: `critical` (smoke), `medium` (валидация), `security` (auth/ownership).

Подробнее про код: [`architecture.md`](architecture.md).

---

## Подготовка

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Unix:     source .venv/bin/activate

pip install -r requirements.txt
# для mypy / pre-commit:
make install-dev
# или: pip install -r requirements-dev.txt && pre-commit install
```

```bash
# Windows
copy .env.example .env
# Unix
cp .env.example .env
```

| Переменная | Назначение |
|------------|------------|
| `BASE_URL` | базовый URL API |
| `TEST_USERNAME` | имя для `POST /authorize` |
| `TEST_TOKEN` | сохранённый токен (если жив — переиспользуется) |

`.env` не коммитится. Для Allure HTML нужен Allure CLI (`make allure`).

---

## Что происходит при `make test` / `pytest`

1. Pytest читает `pytest.ini` (`tests/`, `pythonpath=.`, `--alluredir=./allure-results`, `--clean-alluredir`).
2. Session-фикстура `auth_token`: живой `TEST_TOKEN` или новый authorize.
3. Клиенты эндпоинтов получают токен.
4. `meme_fixture` при необходимости создаёт мем и удаляет в teardown (если не `skip_cleanup`).
5. Вызов → `_make_request` → HTTP + Allure attachments → `check_*`.

---

## Команды Make (канон)

| Команда | Что делает |
|---------|------------|
| `make install` | `pip install -r requirements.txt` |
| `make install-dev` | runtime + mypy/pre-commit + git hooks |
| `make lint` / `make mypy` | статическая проверка типов (mypy) |
| `make pre-commit` | все pre-commit хуки на всех файлах |
| `make pre-commit-run` | алиас `pre-commit` |
| `make pre-commit-install` | только установка git hooks |
| `make test` | весь suite |
| `make critical` | `@pytest.mark.critical` |
| `make medium` | `@pytest.mark.medium` |
| `make security` | `@pytest.mark.security` |
| `make authorize` / `get` / `post` / `put` / `delete` / `e2e` | один файл тестов |
| `make marker M=security` | произвольный маркер |
| `make file F=tests/test_memes_get.py` | произвольный файл |
| `make failed` | только упавшие (`--lf`) |
| `make last` | стоп на первом падении (`-x`) |
| `make allure` | сгенерировать и открыть HTML-отчёт |
| `make allure-gen` | только generate |
| `make clean` | кэши и артефакты отчётов |

Без Make:

```bash
python -m pytest
python -m pytest -m critical
python -m pytest tests/test_memes_post.py
python -m mypy
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## Схема «от команды до отчёта»

```text
activate venv → .env → make test / pytest
                         → allure-results/
                         → make allure → браузер
```

Падения: [`test-analysis.md`](test-analysis.md), [`troubleshooting.md`](troubleshooting.md).
