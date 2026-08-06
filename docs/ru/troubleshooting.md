# Troubleshooting

Типичные проблемы и быстрые решения.  
Как **системно** разбирать падение теста: [`test-analysis.md`](test-analysis.md).  
Установка и команды: [`local-run.md`](local-run.md), [`quick-start.md`](quick-start.md).

**Язык:** Русский · [English](../en/troubleshooting.md)

---

## Таблица симптом → решение

| Симптом | Типичная причина | Решение |
|---------|------------------|---------|
| `BASE_URL is not set` | нет `.env` или пустой `BASE_URL` | скопировать `.env.example` → `.env` и заполнить; в CI — Secrets |
| Сеть / timeout / connection | стенд недоступен, неверный URL | проверить `BASE_URL` в браузере/curl |
| `401` на CRUD | мёртвый, пустой или убитый токен | перевыпустить через authorize; не использовать session-токен в kill-тесте |
| `403` на PUT/DELETE | вызывающий не владелец мема | для чужого пользователя — ожидаемо; свой ресурс — `meme_fixture` |
| `404` на GET/DELETE | нет мема / уже удалён | проверить id; повторный DELETE → `404` по контракту |
| `400` на POST/PUT | валидация тела | сверить payload с [`qa-requirements.md`](qa-requirements.md); для PUT — существующий id |
| Фикстура `meme_fixture` падает на setup | create не вернул int id | смотреть Allure attach create; доступность API |
| mypy / `make lint` red | типы / incomplete defs | исправить по выводу; `make pre-commit` |
| pre-commit red | хук (whitespace, mypy, …) | читать вывод хука; [`pre-commit.md`](pre-commit.md) |
| Allure не открывается | нет Allure CLI | `npm install -g allure-commandline` (или аналог ОС); затем `make allure` |
| Пустой / странный Allure | прогон без `--alluredir` или очистка | гонять через `pytest`/`make test` из проекта (`pytest.ini`) |
| CI red на mypy | те же ошибки типов | локально `make lint` до push ([`ci-cd.md`](ci-cd.md)) |
| CI red на pytest | падение тестов / стенд / secrets | Actions → Run API Tests; отчёт на Pages; [`test-analysis.md`](test-analysis.md) |
| CI «зелёный» отчёт, но step pytest красный | `continue-on-error: true` на pytest | смотреть summary step и Allure, не только итоговый deploy |

---

## Быстрые проверки окружения

```bash
# активирован ли venv и видит ли пакеты
python -c "import pytest, requests; print('ok')"

# задан ли BASE_URL (без печати секретов в чат/лог публично)
python -c "from endpoints.constants import BASE_URL; print(bool(BASE_URL))"
```

---

## Куда идти дальше

| Вопрос | Документ |
|--------|----------|
| Как устроен фреймворк | [`architecture.md`](architecture.md) |
| Что должно вернуть API | [`qa-requirements.md`](qa-requirements.md) |
| Как устроен pipeline | [`ci-cd.md`](ci-cd.md) |
| Оглавление | [`index.md`](index.md) |
