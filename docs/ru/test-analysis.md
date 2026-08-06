# Анализ результатов тестов

Как разбирать падения: локально и в CI.  
FAQ «не ставится Allure / нет .env» → [`troubleshooting.md`](troubleshooting.md).  
Ожидаемые коды → [`qa-requirements.md`](qa-requirements.md).

**Язык:** Русский · [English](../en/test-analysis.md)

---

## Процесс разбора (чеклист)

### 1. Идентифицировать тест

- имя функции / parametrize id;
- маркер: `critical` | `medium` | `security`;
- Allure title / feature / story.

### 2. Открыть шаг в Allure

В `_make_request` к шагу прикреплены:

| Attachment | Содержание |
|------------|------------|
| `request` | method, url, headers (`Authorization` → `***`) |
| `request_body` | JSON/текст тела (если было) |
| `response` | status_code, headers |
| `response_body` | JSON или raw text |
| `network_error` | если упал requests |

Сравните фактический status/body с таблицей в [`qa-requirements.md`](qa-requirements.md).

### 3. Отделить известный дефект

| Сигнал | Значение |
|--------|----------|
| `xfail` на `test_update_meme_response_id_is_int` | BUG-001: PUT возвращает `id` как `string` — **ожидаемо** |
| strict xfail стал unexpected pass | баг на стенде **исправлен** — обновить тесты/доки |

Не маскировать BUG-001 через `str(actual) == str(expected)`.

### 4. Где смотреть отчёт

| Среда | Как |
|-------|-----|
| Локально | после прогона: `make allure` (нужен Allure CLI) |
| CI | GitHub Pages (environment **github-pages**) или artifact `allure-results-raw` |
| CI логи | Actions → job **Run API Tests** → step pytest / mypy |

Пайплайн: [`ci-cd.md`](ci-cd.md).

### 5. Типичная классификация причин

| Наблюдение | Куда смотреть |
|------------|----------------|
| Неверный статус vs контракт | `qa-requirements.md`, request/response body |
| `401` на CRUD | токен / Secrets / kill не того токена |
| `403` на PUT/DELETE | ownership (other user) — часто ожидаемо |
| `404` | id не существует или уже удалён |
| Падение в setup фикстуры | create meme / authorize; смотреть attach setup-шага |
| mypy red, pytest не дошёл | `make lint`, [`pre-commit.md`](pre-commit.md) |

Если симптом известный — таблица в [`troubleshooting.md`](troubleshooting.md).

---

## Фильтрация при повторной проверке

```bash
make critical          # smoke
make security          # auth / ownership
make file F=tests/test_memes_update.py
pytest -k "forbidden" -q
make failed            # только ранее упавшие
```

---

## Связанные документы

- [`architecture.md`](architecture.md) — где в коде attach и asserts  
- [`local-run.md`](local-run.md) — команды  
- [`ci-cd.md`](ci-cd.md) — Jobs и Pages  
