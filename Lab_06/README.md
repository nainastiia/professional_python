# Warehouse Inventory System & Automated Test Suite

Проєкт реалізує **Систему обліку складських запасів** (Варіант 10) та повноцінний автоматизований **Test Suite** із використанням фреймворку `pytest` відповідно до вимог Лабораторної роботи №6.

---

## Особливості системи

- **Моделі та Value Objects**: 
  - `Money` — значення грошових сум із перевіркою від'ємних значень та контролем валют.
  - `WarehouseItem` — сутність товару з підтримкою операцій надходження (`receive`) та списання (`issue`).
- **Сервісна логіка**:
  - Обчислення загальної вартості складських залишків.
  - Фільтрація товарів із низьким рівнем залишків (`low stock`).
  - Потоковий CSV-імпорт (`stream_import_csv`) із валідацією записів.
  - JSON-експорт звітів.
- **Обробка винятків**:
  - `InsufficientStockError` — нестача товару при списанні.
  - `MalformedRecordError` — пошкоджені записи при імпорті.
- **Гнучке налаштування**:
  - Динамічне зчитування порогу залишків через змінну середовища `LOW_STOCK_THRESHOLD`.

---

## Структура проєкту

```text
warehouse_project/
├── pyproject.toml
├── README.md
├── src/
│   └── warehouse/
│       ├── __init__.py
│       ├── exceptions.py
│       ├── value_objects.py
│       ├── models.py
│       ├── services.py
│       ├── repositories.py
│       ├── exporters.py
│       └── protocols.py
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── test_money.py
    │   ├── test_warehouse_item.py
    │   ├── test_warehouse_service.py
    │   └── test_exporters.py
    └── integration/
        └── test_stock_pipeline.py
```

## Інсталяція та налаштування
- **Клонування / Створення середовища**
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/macOS
# або .venv\Scripts\activate для Windows
```
-**Встановлення залежностей проєкту**
```bash
pip install -e ".[dev]"
```
-**Запуск усіх тестів**
```bash
pytest
```
-**Запуск у деталізованому режимі (Verbose)**
```bash
pytest -v
```
-**Запуск із підрахунком покриття коду**
```bash
pytest -v --cov=warehouse --cov-branch --cov-report term-missing
```
-**Генерація HTML-звіту покриття**
```bash
pytest --cov=warehouse --cov-branch --cov-report=html
```
-Після виконання відкрийте htmlcov/index.html у своєму браузері.