# Warehouse Management System (REST API) - Variant 10

Система обліку складських запасів із підтримкою асинхронного REST API, створена за допомогою FastAPI, Pydantic, SQLAlchemy та HTTPX.

## Структура проєкту

- `src/warehouse_system/database.py` — налаштування з'єднання з БД та SQLAlchemy session.
- `src/warehouse_system/models.py` — SQLAlchemy ORM-моделі `Product` та `StockOperation`.
- `src/warehouse_system/schemas.py` — Pydantic-схеми для валідації та серіалізації даних.
- `src/warehouse_system/repositories.py` — Repository Layer для ізольованої роботи з БД.
- `src/warehouse_system/services.py` — Service Layer для бізнес-логіки та асинхронних операцій.
- `src/warehouse_system/api.py` — FastAPI застосунок та REST endpoints.
- `src/warehouse_system/external_api.py` — асинхронні HTTP-запити через HTTPX (gather, Task, Semaphore, retry, timeout).
- `tests/` — автоматизовані тести API та бізнес-логіки.

## Інструкція з запуску

1. Встановлення залежностей:
```bash
pip install -e .[test]
```
## Запуск сервера розробки:
```bash
uvicorn warehouse_system.api:app --reload
```

## Інтерактивна документація Swagger:
Відкрийте у браузері: http://127.0.0.1:8000/docs

## Запуск автоматизованих тестів:
```bash
pytest -v
```