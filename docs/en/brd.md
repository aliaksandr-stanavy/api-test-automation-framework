# BRD — Memes API

**Business Requirements Document** — *what* the system must do.  
No automation details, error status codes, or CI infrastructure.

**Language:** [Русский](../ru/brd.md) · English

| Document | Role |
|----------|------|
| **This file (`brd.md`)** | business requirements: capabilities, data model, endpoint catalog |
| [`qa-requirements.md`](qa-requirements.md) | QA contract: expected codes, negatives, markers, fixtures, known bugs |

---

## 1. Purpose

The Memes REST API allows you to:

1. authorize a user and obtain an access token;
2. check that a token is still valid;
3. manage the **Meme** entity: list, get by id, create, update, delete.

| Parameter | Requirement |
|-----------|-------------|
| API style | REST |
| Body format | JSON |
| Base URL | provided by environment (concrete value is out of BRD scope) |

---

## 2. Access

All resource operations are available to **authorized** users only.

| Header | Value |
|--------|-------|
| `Authorization` | token issued by `POST /authorize` |

```http
Authorization: <token>
```

Tokens are obtained via `POST /authorize` (`name` field: string).

> How tokens are reused in automation and which HTTP codes to expect on access denial — see [`qa-requirements.md`](qa-requirements.md).

---

## 3. Data model: Meme

| Field | Type | Required | Where used | Description |
|-------|------|----------|------------|-------------|
| `id` | `int` | yes | API response; **PUT** body | Meme identifier |
| `text` | `string` | yes | POST, PUT | Meme text |
| `url` | `string` | yes | POST, PUT | Image / resource URL |
| `tags` | `array` | yes | POST, PUT | List of tags |
| `info` | `object` | yes | POST, PUT | Extra metadata |

Rules:

- on **create** (`POST /meme`), `id` must **not** be sent in the body — the server assigns it;
- on **update** (`PUT /meme/<id>`), `id` in the body is **required** and must be type **`int`**;
- the BRD does **not** forbid additional request body fields beyond those listed.

---

## 4. Endpoint catalog

Brief: purpose and required fields. Expected response statuses and negative scenarios — [`qa-requirements.md`](qa-requirements.md).

### 4.1. Authorization

| Method / Path | Purpose | Body |
|---------------|---------|------|
| `POST /authorize` | Issue a token | `name: string` (required) |
| `GET /authorize/<token>` | Check whether the token is alive | — |

### 4.2. Memes (CRUD)

All methods below require the `Authorization` header.

| Method / Path | Purpose | Body (all fields required) |
|---------------|---------|----------------------------|
| `GET /meme` | List all memes | — |
| `GET /meme/<id>` | One meme by id | — |
| `POST /meme` | Create a meme | `text`, `url`, `tags`, `info` |
| `PUT /meme/<id>` | Update a meme | `id` (`int`), `text`, `url`, `tags`, `info` |
| `DELETE /meme/<id>` | Delete a meme | — |

---

## 5. `id` type requirement

The meme `id` field in every response where it appears must be type **`int`**, including after a successful `PUT /meme/<id>`.

Violating this (for example, `id` as a string in a PUT response) is a **product defect**.  
How the defect is tracked in automation — see BUG-001 in [`qa-requirements.md`](qa-requirements.md).

---

## 6. Out of scope for this BRD

The following is **not** described here (lives in QA docs / stand observations):

- exact HTTP error codes (`400` / `401` / `403` / `404`);
- service endpoint `GET /authorize/kill/<token>`;
- ownership rules (meme owner vs another user);
- Pytest marker matrix, fixtures, Allure, CI.
