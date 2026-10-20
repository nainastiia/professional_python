# Система обліку складських запасів (Warehouse Management System)

Лабораторна робота №6 з дисципліни «Професійний Python»  
**Варіант №10:** Система обліку складських запасів.

---

## Опис проєкту

Даний проєкт є системою автоматизованого тестування для доменної моделі та сервісів системи обліку складських запасів. В рамках роботи реалізовано:
- Доменні моделі товарів (`WarehouseItem`) та контейнера складу (`Warehouse`) з повною валідацією атрибутів.
- Сервіси бізнес-логіки для пошуку, розрахунку вартості інвентарю та визначення позицій із низьким запасом.
- Універсальне сховище в пам'яті (`InMemoryRepository`) на базі Generics.
- Модулі імпорту та експорту даних у формати CSV та JSON (`CSVExporter`, `CSVImporter`, `JSONExporter`).
- Асинхронний сервіс замовлення товарів (`AsyncReorderService`).
- Повний набір unit- та integration-тестів з використанням `pytest`, `fixtures`, `tmp_path`, `monkeypatch`, `Mock` та `AsyncMock`.

---

## Структура проєкту

```text
warehouse_project/
├── pyproject.toml
├── README.md
├── src/
│   └── application/
│       ├── __init__.py          # Ініціалізація пакета та експорт компонентів
│       ├── models.py            # Доменні моделі (WarehouseItem, Warehouse)
│       ├── config.py            # Конфігурація застосунку та змінні оточення
│       ├── repositories.py      # Універсальне сховище InMemoryRepository
│       ├── services.py          # Бізнес-логіка та асинхронні сервіси
│       └── exporters.py         # Експорт/імспорт у CSV та JSON
└── tests/
    ├── conftest.py             # Спільні фікстури pytest (sample_item, sample_warehouse)
    ├── unit/
    │   ├── test_models.py      # Модульні тести моделей
    │   ├── test_validators.py  # Тести валідації та boundary cases (@pytest.mark.parametrize)
    │   └── test_services.py    # Тести сервісів, Mock, side_effect та AsyncMock
    └── integration/
        ├── test_configuration.py # Інтеграційні тести конфігурації (monkeypatch)
        └── test_import_export.py # Інтеграційні тести імпорту/експорту (tmp_path)
```

## Створення та активація віртуального середовища
```bash
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
```

## Встановлення проєкту та dev-залежностей
```bash
python -m pip install -e ".[dev]"
```

## Запуск тестів та перевірка покриття
```bash
pytest -v --cov=application --cov-branch --cov-report term-missing --cov-report=html
```