# Быстрый старт

Цель: увидеть **зелёный** прогон за несколько минут. Подробности — в [`local-run.md`](local-run.md).

**Язык:** Русский · [English](../en/quick-start.md)

## 1. Что нужно

- Python 3.12+
- доступ к Memes API (`BASE_URL`)
- (опционально) Make

## 2. Установка

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

Заполните в `.env`: `BASE_URL`, `TEST_USERNAME`, `TEST_TOKEN`.
Шаблон: [`.env.example`](../../.env.example) (`BASE_URL=https://api.example.com` — замените на URL своего стенда).

## 3. Самый быстрый прогон

```bash
pytest -m critical -q
# или:
make critical
```

Ожидание: critical-тесты `passed` (один `xfail` на PUT `id` — известный баг API, см. [`qa-requirements.md`](qa-requirements.md)).

## 4. Минимальный пример теста

Пример в стиле проекта (Page Object + checks). Файл в suite добавлять не обязательно — достаточно понять паттерн:

```python
from endpoints.authorize import Authorize


def test_authorize_smoke():
    auth = Authorize()
    auth.authorize("demo_user")
    auth.check_status_is_200()
    auth.check_response_is_json()
    assert auth.json.get("token"), "token missing"
```

Запуск одного такого файла:

```bash
pytest path/to/your_smoke.py -q
```

### Ожидаемый результат

| Исход | Что это значит |
|-------|----------------|
| Тест зелёный | API доступен, authorize вернул токен |
| `BASE_URL is not set` | нет или пустой `.env` → [`troubleshooting.md`](troubleshooting.md) |
| `401` / сеть | проверьте URL и доступность стенда |

## 5. Полезные команды

| Команда | Что делает |
|---------|------------|
| `make test` | весь suite |
| `make critical` | только `@pytest.mark.critical` |
| `make allure` | HTML-отчёт Allure |
| `make pre-commit` | все pre-commit хуки |

Полный список Make: [`local-run.md`](local-run.md).

## Дальше

- Как устроен код → [`architecture.md`](architecture.md)
- Падения и FAQ → [`troubleshooting.md`](troubleshooting.md)
- Оглавление → [`index.md`](index.md)
