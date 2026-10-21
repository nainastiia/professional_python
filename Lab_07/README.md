# Warehouse System

Консольний застосунок для обліку складських запасів (Варіант 10) з дисципліни «Професійний Python», доповнений шаром збереження даних (Persistence Layer), SQLAlchemy ORM, міграціями Alembic та інтеграційними тестами.

## Структура проєкту
Проєкт організовано за стандартом `src-layout`:
```text
warehouse_system/
├── pyproject.toml
├── README.md
├── .gitignore
├── alembic.ini
├── migrations/
│   ├── env.py
│   └── versions/
│       └── ..._add_minimum_stock.py
├── src/
│   └── warehouse_system/
│       ├── __init__.py
│       ├── database.py
│       ├── models.py
│       ├── repositories.py
│       ├── services.py
│       ├── db_api.py
│       └── main.py
└── tests/
    ├── conftest.py
    └── test_repositories.py
```
## Створіть та активуйте віртуальне середовище:
```bash
python -m venv .venv
# Для Windows: .venv\Scripts\activate
# Для Linux/macOS: source .venv/bin/activate
```
## Встановіть пакет разом із залежностями та інструментами для тестування:
```bash
python -m pip install -e ".[test]"
```
## Ініціалізуйте міграції
```bash
alembic init migrations
```
## Застосуйте міграції для оновлення структури таблиць
```bash
alembic upgrade head
```
## Запуск програми
```bash
python -m warehouse_system.main
```
## Запуск тестування
```bash
pytest -v
```