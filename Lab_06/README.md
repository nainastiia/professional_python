# Lab 06 — Варіант 10: Система обліку складських запасів

Самостійна навчальна реалізація, не оригінальний код Lab_01.

## Основні сутності
- `Product`: довідник товарів;
- `WarehouseItem`: облік `quantity`, `unit_price`;
- `WarehouseRepository`: збереження і пошук записів;
- `Warehouse`: операції `stock` (надходження, списання), контроль `low-stock`;
- `low_stock_threshold`: параметр `threshold` зі змінної середовища;
- `read_items`: потоковий `csv` імпорт;
- `export_json`: `json` експорт.

## Запуск

```bash
python -m pip install -e ".[dev]"
python -m pytest -v --cov=warehouse --cov-branch --cov-report=term-missing --cov-report=html
```

Звіт покриття: `htmlcov/index.html`.
