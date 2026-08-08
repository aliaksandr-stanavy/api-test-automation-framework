# 🧪 Memes API — Test Automation

**Язык:** Русский · [English](README.en.md)

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.1-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.15.2-purple?logo=allure&logoColor=white)](https://allurereport.org/)
[![CI](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-GitHub%20Pages-orange?logo=allure&logoColor=white)](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aliaksandr--stanavy-181717?logo=github&logoColor=white)](https://github.com/aliaksandr-stanavy)

**API test automation framework** для Memes API на Python + Pytest + Allure + Requests.

> Этот проект — **демонстрация промышленного подхода** к тестированию API: чистая архитектура, глубокая проверка безопасности, автоматическая отчётность и полноценный CI/CD.

| Старт | Документация |
|-------|----------------|
| [Быстрый старт](docs/ru/quick-start.md) (~5 мин) | [Оглавление RU](docs/ru/index.md) · [EN](docs/en/index.md) · [языки](docs/README.md) |

---

## 📖 О проекте

Фреймворк показывает, как выстроить инфраструктуру API-автоматизации с акцентом на **надёжность, поддерживаемость и прозрачность результатов**.

**Ключевые возможности:**
- 🏗️ **Page Object для API** — чёткая архитектура клиентов.
- 📊 **Allure-отчёты** — с шагами, вложениями request/response и маскированием токенов.
- 🏷️ **Маркеры приоритетов** (`critical` / `medium` / `security`) для гибкого запуска.
- 🔒 **Security-сценарии** — проверка `401`/`403` с подтверждением, что данные **не изменились**.
- ⚙️ **CI/CD** — GitHub Actions с автоматической публикацией отчёта на GitHub Pages.
- 🎲 **Генерация данных** (Faker) и **polling** (Tenacity) для тестов с ожиданием.
- 🛡️ **Статический анализ** — mypy + TypedDict, pre-commit хуки в CI.

### 🔥 Что именно демонстрирую

- **Ресурсную изоляцию:** сессионный токен, disposable kill-токен и гарантированный teardown мемов (даже при падении теста).
- **Security глубже статус-кода:** проверяем не только `401`/`403`, но и что ресурс **реально не изменился**.
- **Известный дефект API:** зафиксирован через `xfail` (PUT возвращает `id` как string).
- **Качество кода:** типизация клиентов и payload (mypy + TypedDict), pre-commit в CI.
- **Полный контур отчёта:** Allure → GitHub Actions → GitHub Pages.

---

## 🛠 Стек

| Компонент | Технология |
|-----------|------------|
| 🐍 Язык | Python 3.12+ |
| 🧪 Тест-раннер | Pytest 9.0.1 |
| 🌐 HTTP-клиент | Requests 2.32.4 |
| 📊 Отчёты | allure-pytest 2.15.2 |
| 🎲 Генерация данных | Faker 38.2.0 |
| 🔁 Retry / polling | Tenacity 9.1.2 |
| 🛡️ Типы / хуки | mypy, TypedDict, pre-commit |
| ⚙️ CI/CD | GitHub Actions → Allure на Pages |
| 🔗 Стенд | Memes API (URL задаётся в `.env` / Secrets как `BASE_URL`) |

---

## 🚀 Быстрый старт

```bash
git clone https://github.com/aliaksandr-stanavy/api-test-automation-framework.git
cd api-test-automation-framework

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # или: cp .env.example .env
# заполните BASE_URL, TEST_USERNAME, TEST_TOKEN (опционально)

make critical
# или: pytest -m critical -q
```

| Переменная | Описание |
|------------|----------|
| `BASE_URL` | базовый URL Memes API |
| `TEST_USERNAME` | имя для `POST /authorize` |
| `TEST_TOKEN` | сохранённый токен (если жив — переиспользуется) |

В CI — **GitHub Secrets**. Полный гайд: [quick-start](docs/ru/quick-start.md) · Make и Allure: [local-run](docs/ru/local-run.md).

---

## 📁 Структура

```text
api-test-automation-framework/
├── endpoints/           # API clients + общие asserts
├── tests/               # сценарии
├── utils/               # generators, cases, TypedDict
├── conftest.py          # фикстуры
├── Makefile
├── docs/
│   ├── README.md        # навигатор языков
│   ├── ru/              # документация (RU)
│   └── en/              # документация (EN)
├── .github/workflows/   # CI/CD
├── LICENSE
└── CHANGELOG.md
```

---

## 📚 Документация

Полное оглавление: **[docs/ru/index.md](docs/ru/index.md)**. Ниже — навигация по документации.

### Навигация по документации

| Если вам нужно... | Документ | ⏱ Примерное время |
|---|---|---|
| **Запустить тесты** | [Быстрый старт](docs/ru/quick-start.md) | ~5 минут |
| **Понять устройство кода** | [Архитектура](docs/ru/architecture.md) | 15 минут |
| **Выбрать фикстуру** | [Справочник фикстур](docs/ru/fixtures-reference.md) | 10 минут |
| **Узнать контракт продукта** | [BRD](docs/ru/brd.md) | 10 минут |
| **Проверить ожидаемые коды** | [QA-требования](docs/ru/qa-requirements.md) | 10 минут |
| **Узнать все Make-команды** | [Локальный запуск](docs/ru/local-run.md) | 5 минут |
| **Разобрать красный CI** | [CI/CD](docs/ru/ci-cd.md) + [Анализ результатов](docs/ru/test-analysis.md) | 15 минут |
| **Решить проблему** | [Troubleshooting](docs/ru/troubleshooting.md) | 5 минут |

История изменений: [CHANGELOG.md](CHANGELOG.md).

---

## ✅ Что покрыто

- Authorize, CRUD meme, E2E lifecycle  
- Валидация полей и invalid ids  
- Security: `401` без/с неверным токеном; `403` для non-owner + проверка, что ресурс не затронут  
- Известный баг: PUT `id` как `string` — `xfail` (см. [qa-requirements](docs/ru/qa-requirements.md))

Тесты интеграционные: нужен доступный API. Allure в `_make_request` прикрепляет request/response (`Authorization` маскируется). Kill-тест использует disposable token — session `auth_token` не убивается.

---

## 📊 Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
# или: make allure
```

В CI отчёт публикуется на **GitHub Pages**:
[https://aliaksandr-stanavy.github.io/api-test-automation-framework/](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
Подробнее: [local-run](docs/ru/local-run.md), [ci-cd](docs/ru/ci-cd.md).

---

## 👤 Автор

Этот проект создан в рамках развития моей экспертизы в **Full Stack QA** и является частью моего публичного **GitHub-портфолио**.
Его цель — показать современные подходы к построению API-фреймворков, организации тестов и CI/CD.

Буду рад обратной связи, предложениям и профессиональному общению.

- 🌐 **GitHub Portfolio:** https://github.com/aliaksandr-stanavy
- 💼 **LinkedIn:** https://www.linkedin.com/in/aliaksandr-stanavy/
- 📧 **Email:** aliaksandr.stanavy@gmail.com

---

## 📄 Лицензия

Проект распространяется по лицензии **MIT**.

Подробности см. в файле [LICENSE](LICENSE).

© 2026 Aliaksandr Stanavy
