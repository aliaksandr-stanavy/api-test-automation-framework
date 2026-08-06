# Справочник фикстур

Каталог Pytest-фикстур проекта: scope, что отдают, когда использовать.

**Язык:** Русский · [English](../en/fixtures-reference.md)

Исходник: [`../../conftest.py`](../../conftest.py) (+ локальная `auth_api` в authorize-тестах).  
Архитектура: [`architecture.md`](architecture.md).

---

## Как выбрать фикстуру

| Задача | Фикстура |
|--------|----------|
| Нужен только строковый токен | `auth_token` |
| CRUD от имени основного пользователя | `*_endpoint` + при необходимости `meme_fixture` |
| Тест сам удаляет мем | `meme_fixture` → в конце `skip_cleanup = True` |
| Много PUT-негативов (только status) | `shared_meme_for_put_negatives` |
| Нет токена / неверный токен | `as_client` + `indirect=True` |
| Чужой пользователь (ownership 403) | `other_user_token` |
| Свежий клиент Authorize | `auth_api` (в `test_memes_authorize.py`) |

Хелпер (не фикстура): `create_endpoint_with_token(cls, token)` — собирает клиент с `Authorization`.

---

## Токены

### `auth_token` — `scope=session`

| | |
|--|--|
| **Отдаёт** | `str` — валидный токен |
| **Логика** | если `TEST_TOKEN` жив (`GET /authorize/<token>` → 200) — его; иначе `POST /authorize` |
| **Использовать** | все CRUD-фикстуры; обычные authenticated-тесты |
| **Не использовать** | в kill-тестах — убивать только disposable-токен |

### `other_user_token` — `scope=session`

| | |
|--|--|
| **Отдаёт** | `str` — токен пользователя `{TEST_USERNAME}_other` |
| **Использовать** | PUT/DELETE «не владелец» → ожидание `403` |
| **Не использовать** | как основной токен для create/cleanup «своих» мемов |

---

## Аутентифицированные клиенты — `scope=function`

Все зависят от `auth_token`, каждый тест получает **новый** экземпляр клиента.

| Фикстура | Класс | Типичное применение |
|----------|-------|---------------------|
| `create_meme_endpoint` | `CreateMeme` | POST /meme |
| `get_all_memes_endpoint` | `GetAllMemes` | GET /meme (список) |
| `get_meme_by_id_endpoint` | `GetMemeById` | GET /meme/\<id\> |
| `update_meme_endpoint` | `UpdateMeme` | PUT /meme/\<id\> |
| `delete_meme_endpoint` | `DeleteMeme` | DELETE /meme/\<id\> |

---

## Данные мема

### `meme_fixture` — `scope=function`

Создаёт мем через `create_meme_endpoint`, в teardown удаляет (если не отключено).

**Yield — `dict`:**

| Ключ | Тип / смысл |
|------|-------------|
| `id` | `int` — id созданного мема (assert на setup) |
| `data` | payload, ушедший в POST |
| `response` | JSON ответа create |
| `skip_cleanup` | `bool`, по умолчанию `False` |

```python
def test_delete_meme(..., meme_fixture):
    ...
    meme_fixture["skip_cleanup"] = True  # тест уже удалил мем
```

**Когда:** happy-path update/get/delete/e2e, security с существующим id.  
**Не когда:** десятки негативных PUT подряд — дорогой create/delete на каждый кейс → см. ниже.

### `shared_meme_for_put_negatives` — `scope=module`

Один мем на модуль для status-only негативов PUT.

**Yield — `dict`:** `id`, `data` (без `skip_cleanup`; teardown всегда DELETE).

**Когда:** `test_update_meme_negative_validation`.  
**Не когда:** тест **успешно** меняет мем и потом читает поля — нужен свежий `meme_fixture`.

---

## Security: `as_client`

**Scope:** function (по умолчанию).  
**Тип:** indirect parametrize.

```python
@pytest.mark.parametrize(
    "as_client",
    [
        (CreateMeme, None),                    # нет Authorization
        (CreateMeme, INVALID_AUTH_TOKEN),      # битый токен
    ],
    indirect=True,
    ids=["no_token", "invalid_token"],
)
def test_create_meme_unauthorized(self, as_client):
    as_client.create_meme(...)
    as_client.check_status_is_401()
```

| `request.param` | Результат |
|-----------------|-----------|
| `(EndpointCls, None)` | клиент без заголовка Authorization |
| `(EndpointCls, token)` | клиент с этим токеном |

Ожидания по кодам: [`qa-requirements.md`](qa-requirements.md).

---

## Локальная фикстура authorize-тестов

### `auth_api` — `scope=function`

Файл: `tests/test_memes_authorize.py`.

| | |
|--|--|
| **Отдаёт** | новый `Authorize()` без общего токена |
| **Зачем** | изоляция authorize/kill от session `auth_token` |

Kill: authorize disposable name → `delete_token` → `wait_until_deleted` — **не** передавать `auth_token`.

---

## Зависимости (схема)

```text
auth_token (session)
├── create_meme_endpoint / get_* / update_* / delete_* (function)
├── meme_fixture (function) ← create_meme_endpoint
└── shared_meme_for_put_negatives (module)

other_user_token (session)     — отдельно
as_client (indirect)           — без auth_token
auth_api (function, local)     — без auth_token
```

---

## Частые ошибки

| Ошибка | Как правильно |
|--------|----------------|
| Kill session-токена | disposable authorize в тесте |
| PUT-негативы на `meme_fixture` × N | `shared_meme_for_put_negatives` |
| Забыли `skip_cleanup` после своего DELETE | teardown может лишний раз DELETE (обычно ок 404), лучше выставить флаг |
| `as_client` без `indirect=True` | parametrize не соберёт клиент |
| Ownership-тест с тем же токеном | нужен `other_user_token` |

Падения setup/teardown: [`test-analysis.md`](test-analysis.md), [`troubleshooting.md`](troubleshooting.md).
