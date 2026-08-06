# Memes API — Test Automation

**Язык:** Русский · [English](README.en.md)

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.1-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.15.2-purple?logo=allure&logoColor=white)](https://allurereport.org/)
[![CI](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/aliaksandr-stanavy/api-test-automation-framework/actions/workflows/api-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-GitHub%20Pages-orange?logo=allure&logoColor=white)](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aliaksandr--stanavy-181717?logo=github&logoColor=white)](https://github.com/aliaksandr-stanavy)

**API test automation framework** для Memes API на Python + Pytest + Allure + Requests.

| Старт | Документация |
|-------|----------------|
| [Быстрый старт](docs/ru/quick-start.md) (~5 мин) | [Оглавление RU](docs/ru/index.md) · [EN](docs/en/index.md) · [языки](docs/README.md) |

---

## О проекте

Демонстрационный фреймворк автоматизации API-тестов. Показывает, как выстроить инфраструктуру с:

- чёткой архитектурой (Page Object для API);
- Allure-отчётами с шагами и вложениями request/response;
- маркерами приоритета (`critical` / `medium` / `security`);
- позитивными, негативными и security/ownership-сценариями;
- CI/CD через GitHub Actions и публикацией отчёта на Pages;
- генерацией данных (Faker) и polling после kill token (Tenacity);
- статическими проверками (mypy + TypedDict) и pre-commit хуками.

### Что демонстрирую

- изоляцию ресурсов: session-токен, disposable kill-token, teardown мемов даже при падении теста;
- security глубже статус-кода: `401`/`403` + проверка, что данные не изменились / мем не удалён;
- известный дефект API зафиксирован через `xfail` (PUT возвращает `id` как string);
- типизацию клиентов и payload (mypy + TypedDict) и pre-commit в CI;
- полный контур отчёта: Allure (request/response, маскирование токена) → GitHub Actions → Pages.

---

## Стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.12+ |
| Тест-раннер | Pytest 9.0.1 |
| HTTP-клиент | Requests 2.32.4 |
| Отчёты | allure-pytest 2.15.2 |
| Генерация данных | Faker 38.2.0 |
| Retry / polling | Tenacity 9.1.2 |
| Типы / хуки | mypy, TypedDict, pre-commit |
| CI/CD | GitHub Actions → Allure на Pages |
| Стенд | Memes API (URL задаётся в `.env` / Secrets как `BASE_URL`) |

---

## Быстрый старт

```bash
git clone https://github.com/aliaksandr-stanavy/api-test-automation-framework.git
cd api-test-automation-framework

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # или: cp .env.example .env
# заполните BASE_URL, TEST_USERNAME, TEST_TOKEN

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

## Структура

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

Устройство кода и фикстур: [architecture](docs/ru/architecture.md) · [fixtures-reference](docs/ru/fixtures-reference.md).

---

## Документация

Полное оглавление: **[docs/ru/index.md](docs/ru/index.md)**. Ниже — тот же порядок чтения и вход по задаче.

### Порядок чтения

1. [Быстрый старт](docs/ru/quick-start.md) — результат за ~5 минут  
2. [Архитектура](docs/ru/architecture.md) — как устроен код  
3. [Справочник фикстур](docs/ru/fixtures-reference.md) — какие фикстуры и когда  
4. [BRD](docs/ru/brd.md) — *что* умеет API  
5. [QA-требования](docs/ru/qa-requirements.md) — *как* тестируем  
6. [Локальный запуск](docs/ru/local-run.md) — Make, pytest, Allure  
7. [Pre-commit](docs/ru/pre-commit.md) — хуки перед коммитом  
8. [CI/CD](docs/ru/ci-cd.md) — GitHub Actions  
9. [Анализ результатов](docs/ru/test-analysis.md) — как разбирать падения  
10. [Troubleshooting](docs/ru/troubleshooting.md) — типичные проблемы  

История изменений: [CHANGELOG.md](CHANGELOG.md).

### По задаче

| Нужно | Документ |
|-------|----------|
| Запустить тесты сейчас | [quick-start](docs/ru/quick-start.md) |
| Понять устройство кода | [architecture](docs/ru/architecture.md) |
| Какую фикстуру взять | [fixtures-reference](docs/ru/fixtures-reference.md) |
| Контракт продукта | [brd](docs/ru/brd.md) |
| Ожидаемые коды и маркеры | [qa-requirements](docs/ru/qa-requirements.md) |
| Все Make-команды | [local-run](docs/ru/local-run.md) |
| Разобрать красный CI | [ci-cd](docs/ru/ci-cd.md) + [test-analysis](docs/ru/test-analysis.md) |
| «У меня не работает» | [troubleshooting](docs/ru/troubleshooting.md) |

---

## Что покрыто

- Authorize, CRUD meme, E2E lifecycle  
- Валидация полей и invalid ids  
- Security: `401` без/с неверным токеном; `403` для non-owner + проверка, что ресурс не затронут  
- Известный баг: PUT `id` как `string` — `xfail` (см. [qa-requirements](docs/ru/qa-requirements.md))

Тесты интеграционные: нужен доступный API. Allure в `_make_request` прикрепляет request/response (`Authorization` маскируется). Kill-тест использует disposable token — session `auth_token` не убивается.

---

## Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
# или: make allure
```

В CI отчёт публикуется на **GitHub Pages**:
[https://aliaksandr-stanavy.github.io/api-test-automation-framework/](https://aliaksandr-stanavy.github.io/api-test-automation-framework/)
(ссылка станет активной после первого успешного deploy на `main`). Подробнее: [local-run](docs/ru/local-run.md), [ci-cd](docs/ru/ci-cd.md).

---

## Автор и лицензия

Проект создан в рамках развития экспертизы **Full Stack QA | Automation QA**.

- GitHub: [aliaksandr-stanavy](https://github.com/aliaksandr-stanavy)
- LinkedIn: [aliaksandr-stanavy](https://www.linkedin.com/in/aliaksandr-stanavy/)
- License: [MIT](LICENSE) © 2026 Aliaksandr Stanavy
