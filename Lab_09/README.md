# Warehouse System (Варіант 10: Система обліку складських запасів)

Модульна система обліку складських запасів із підтримкою багатопотоковості, багатопроцесності, векторизації через NumPy, профілювання часу/пам'яті та кешування з інвалідацією.

## Встановлення та запуск

```bash
# Створення та активація віртуального середовища
python -m venv .venv
source .venv/bin/activate  # для Linux/macOS
# .venv\Scripts\activate   # для Windows

# Встановлення залежностей
pip install -e ".[dev]"

# Запуск API сервера
uvicorn warehouse_system.main:app --reload

# Запуск тестів
pytest

# Запуск бенчмарків
python benchmarks/benchmark.py

# Запуск профілювання
python -m warehouse_system.profiling