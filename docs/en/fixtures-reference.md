# Fixtures reference

Catalog of project Pytest fixtures: scope, what they yield, when to use them.

**Language:** [Русский](../ru/fixtures-reference.md) · English

Source: [`../../conftest.py`](../../conftest.py) (+ local `auth_api` in authorize tests).  
Architecture: [`architecture.md`](architecture.md).

---

## How to pick a fixture

| Task | Fixture |
|------|---------|
| Need only a token string | `auth_token` |
| CRUD as the main user | `*_endpoint` + `meme_fixture` when needed |
| Test deletes the meme itself | `meme_fixture` → set `skip_cleanup = True` at the end |
| Many PUT negatives (status only) | `shared_meme_for_put_negatives` |
| No token / invalid token | `as_client` + `indirect=True` |
| Another user (ownership 403) | `other_user_token` |
| Fresh Authorize client | `auth_api` (in `test_memes_authorize.py`) |

Helper (not a fixture): `create_endpoint_with_token(cls, token)` — builds a client with `Authorization`.

---

## Tokens

### `auth_token` — `scope=session`

| | |
|--|--|
| **Yields** | `str` — valid token |
| **Logic** | if `TEST_TOKEN` is alive (`GET /authorize/<token>` → 200) — reuse it; else `POST /authorize` |
| **Use for** | all CRUD fixtures; normal authenticated tests |
| **Do not use** | in kill tests — only kill a disposable token |

### `other_user_token` — `scope=session`

| | |
|--|--|
| **Yields** | `str` — token for user `{TEST_USERNAME}_other` |
| **Use for** | PUT/DELETE as non-owner → expect `403` |
| **Do not use** | as the main token for create/cleanup of “own” memes |

---

## Authenticated clients — `scope=function`

All depend on `auth_token`; each test gets a **new** client instance.

| Fixture | Class | Typical use |
|---------|-------|-------------|
| `create_meme_endpoint` | `CreateMeme` | POST /meme |
| `get_all_memes_endpoint` | `GetAllMemes` | GET /meme (list) |
| `get_meme_by_id_endpoint` | `GetMemeById` | GET /meme/\<id\> |
| `update_meme_endpoint` | `UpdateMeme` | PUT /meme/\<id\> |
| `delete_meme_endpoint` | `DeleteMeme` | DELETE /meme/\<id\> |

---

## Meme data

### `meme_fixture` — `scope=function`

Creates a meme via `create_meme_endpoint`, deletes it on teardown (unless skipped).

**Yield — `dict`:**

| Key | Type / meaning |
|-----|----------------|
| `id` | `int` — created meme id (asserted on setup) |
| `data` | payload sent in POST |
| `response` | create response JSON |
| `skip_cleanup` | `bool`, default `False` |

```python
def test_delete_meme(..., meme_fixture):
    ...
    meme_fixture["skip_cleanup"] = True  # test already deleted the meme
```

**When:** happy-path update/get/delete/e2e, security with an existing id.  
**When not:** dozens of PUT negatives in a row — expensive create/delete per case → see below.

### `shared_meme_for_put_negatives` — `scope=module`

One meme per module for status-only PUT negatives.

**Yield — `dict`:** `id`, `data` (no `skip_cleanup`; teardown always DELETE).

**When:** `test_update_meme_negative_validation`.  
**When not:** the test **successfully** updates the meme and then reads fields — use a fresh `meme_fixture`.

---

## Security: `as_client`

**Scope:** function (default).  
**Type:** indirect parametrize.

```python
@pytest.mark.parametrize(
    "as_client",
    [
        (CreateMeme, None),                    # no Authorization
        (CreateMeme, INVALID_AUTH_TOKEN),      # bad token
    ],
    indirect=True,
    ids=["no_token", "invalid_token"],
)
def test_create_meme_unauthorized(self, as_client):
    as_client.create_meme(...)
    as_client.check_status_is_401()
```

| `request.param` | Result |
|-----------------|--------|
| `(EndpointCls, None)` | client without Authorization header |
| `(EndpointCls, token)` | client with that token |

Expected status codes: [`qa-requirements.md`](qa-requirements.md).

---

## Local authorize-test fixture

### `auth_api` — `scope=function`

File: `tests/test_memes_authorize.py`.

| | |
|--|--|
| **Yields** | new `Authorize()` without the shared token |
| **Why** | isolate authorize/kill from session `auth_token` |

Kill: authorize a disposable name → `delete_token` → `wait_until_deleted` — do **not** pass `auth_token`.

---

## Dependency diagram

```text
auth_token (session)
├── create_meme_endpoint / get_* / update_* / delete_* (function)
├── meme_fixture (function) ← create_meme_endpoint
└── shared_meme_for_put_negatives (module)

other_user_token (session)     — separate
as_client (indirect)           — no auth_token
auth_api (function, local)     — no auth_token
```

---

## Common mistakes

| Mistake | Correct approach |
|---------|------------------|
| Killing the session token | disposable authorize in the test |
| PUT negatives on `meme_fixture` × N | `shared_meme_for_put_negatives` |
| Forgot `skip_cleanup` after own DELETE | teardown may DELETE again (usually OK 404); better set the flag |
| `as_client` without `indirect=True` | parametrize will not build the client |
| Ownership test with the same token | need `other_user_token` |

Setup/teardown failures: [`test-analysis.md`](test-analysis.md), [`troubleshooting.md`](troubleshooting.md).
