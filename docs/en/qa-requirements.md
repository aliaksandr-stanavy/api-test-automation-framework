# Memes API — automation requirements (QA)

Document for designing and maintaining automated tests.  
Describes *how we verify* the API: expected codes, negatives, fixtures, markers, known bugs.

**Language:** [Русский](../ru/qa-requirements.md) · English

| Document | Role |
|----------|------|
| [`brd.md`](brd.md) | business requirements: *what* the API does (model, endpoints, auth) |
| **This file (`qa-requirements.md`)** | QA contract: *how* we test and what counts as pass/fail |

Do not duplicate the endpoint field catalog here — it lives in the BRD. Include only what automated tests need beyond the BRD.

How the framework code is structured: [`architecture.md`](architecture.md).

---

## 1. Link to the BRD (brief)

- REST + JSON, header `Authorization: <token>`.
- CRUD memes and authorize — per [`brd.md`](brd.md).
- `id` in responses is **`int`** (including after PUT).
- Extra fields in the body are not forbidden by the BRD → do not expect `400` solely because of an extra field.

Base URL and credentials come from the environment (see [§7](#7-environment-variables)).

---

## 2. Authorization in tests

### 2.1. Token reuse

Tokens on the stand are long-lived. To avoid creating them unnecessarily:

1. `GET /authorize/<token>` for `TEST_TOKEN`;
2. if `200` — reuse it;
3. otherwise — `POST /authorize` with `TEST_USERNAME`.

In the project: fixture `auth_token` (`scope=session`).  
Kill tests use a **separate disposable** token and do not touch the session token.

### 2.2. Expected access-denied codes

| Condition | Expected status | Note |
|---------|------------------|------------|
| No `Authorization` | `401` | strictly 401 |
| Invalid / killed token | `401` | strictly 401 |
| Valid token, but **not the meme owner** (PUT/DELETE) | `403` | observed; not detailed in the BRD |
| `GET /authorize/<nonexistent>` | `404` | “is the token alive” check |

### 2.3. Helper endpoint (not in the BRD)

| Method / Path | Role in tests |
|---------------|---------------------|
| `GET /authorize/kill/<token>` | token invalidation; then poll `GET /authorize/<token>` until `404` (tenacity) |

---

## 3. Model clarifications (test design only)

All field and type details are in [`brd.md` §3](brd.md#3-data-model-meme). For automated tests, what matters:

| Topic | Rule |
|------|---------|
| Required fields | missing / wrong type → expect `400` (POST/PUT) |
| Extra field | not a negative: API accepts it, `200` |
| `id` after PUT | must be `int`; otherwise BUG-001 |
| PUT body validation | path/body must use an **existing** meme id, otherwise often `404` before `400` |

`GET /meme` list response: array at the JSON root **or** under the `data` key (both are acceptable in tests).

A meme response may include a service field such as `updated_by` — that does not affect the successful BRD-field contract.

---

## 4. Endpoint contract (automated test expectations)

Purpose and field sets are in the BRD. Below — **positive / negative / security** for Pytest.

### 4.1. `POST /authorize`

| Scenario | Expectation |
|----------|----------|
| Valid `name` | `200`, body has `token` and `user` (== submitted `name`) |
| `name` wrong type / `null` | `400` |
| Missing `name` field | `400` |
| Empty string `name` | observed: `200`, `user == ""` (captured by a test) |

### 4.2. `GET /authorize/<token>`

| Scenario | Expectation |
|----------|----------|
| Live token | `200`, text contains `Token is alive` and the username |
| Unknown token | `404` |

### 4.3. `GET /meme`

| Scenario | Expectation |
|----------|----------|
| With a valid token | `200`, the created meme is in the list and has BRD fields |
| Without / with a wrong token | `401` |

### 4.4. `GET /meme/<id>`

| Scenario | Expectation |
|----------|----------|
| Existing id | `200`, fields match what was created, `id` is `int` and equals the requested one |
| Nonexistent / invalid id | `404` |
| Without / with a wrong token | `401` |

### 4.5. `POST /meme`

| Scenario | Expectation |
|----------|----------|
| Valid payload | `200`, data in the response, `id: int`, meme is readable via GET |
| Missing required / wrong type | `400` |
| Extra field | `200` (not an error) |
| Without / with a wrong token | `401` |

### 4.6. `PUT /meme/<id>`

| Scenario | Expectation |
|----------|----------|
| Valid update of own meme | `200`, fields as in the request; response `id` is **`int`** |
| Nonexistent id | `404` |
| Missing required / wrong type (on an existing id) | `400` |
| Without / with a wrong token | `401` |
| Another user (not owner) | `403` |

### 4.7. `DELETE /meme/<id>`

| Scenario | Expectation |
|----------|----------|
| Delete own meme | `200`; then GET by id → `404`; meme is absent from the list |
| Delete again | `404` |
| Nonexistent / invalid id | `404` |
| Without / with a wrong token | `401` |
| Another user (not owner) | `403`; meme remains available to the owner |

---

## 5. Pytest marker matrix

| Area | `critical` | `medium` | `security` |
|---------|------------|----------|------------|
| Successful authorize / smoke CRUD / E2E / GET by id | ✓ | | |
| Check token, payload boundaries, validation, 404 | | ✓ | |
| Missing/broken token, kill+poll, ownership 403 | | | ✓ |

---

## 6. Known defects

| ID | Endpoint | Expectation (BRD) | Actual | In tests |
|----|----------|----------------|------|----------|
| BUG-001 | `PUT /meme/<id>` | `id: int` | `id` as `string` | `test_update_meme_response_id_is_int` — `xfail(strict=True)` |

**Do not** mask BUG-001 like this:

```python
assert str(actual_id) == str(expected_id)
```

Required: `isinstance(actual_id, int)` + value comparison.

---

## 7. Environment variables

| Variable | Purpose |
|------------|------------|
| `BASE_URL` | API base URL |
| `TEST_USERNAME` | Name for `POST /authorize` |
| `TEST_TOKEN` | Stored token for reuse |

Template: [`../../.env.example`](../../.env.example). In CI — GitHub Secrets.  
Local run: [`local-run.md`](local-run.md). CI: [`ci-cd.md`](ci-cd.md).

---

## 8. Test design recommendations

1. For PUT negatives on body validation — only an **existing** meme id (`shared_meme_for_put_negatives` / `meme_fixture`).
2. Do not add a negative “extra field → 400”.
3. Do not kill the session token; for kill — disposable user/token.
4. After create in fixtures — teardown `DELETE` (or `skip_cleanup` if the test deleted it itself).
5. Check `id` strictly (`int` + equality), especially after PUT.
6. Status asserts must be exact (`401` vs `403`), no “or”.
7. Assert messages: expected/got + body (and Allure request/response in `_make_request`).
