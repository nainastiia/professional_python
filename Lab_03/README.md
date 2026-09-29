# Потокова обробка складських запасів (Лабораторна робота №3, Варіант 10)

Цей проєкт реалізує потоковий конвеєр (Lazy Pipeline) для обробки великих наборів даних складського обліку без необхідності повної матеріалізації колекцій у пам'яті (Memory-efficient streaming processing).

## Особливості реалізації (Варіант 10)
- **Streaming CSV Reading:** Потокове читання файлів за допомогою генераторів та `yield from`.
- **Validation Stage:** Валідація кількості та ціни товарів з підрахунком кількості коректних і некоректних записів (`valid/invalid records`).
- **Transformations:** Динамічне оновлення кількості товарів (обробка надходжень і списань у потоці).
- **Filtering:** Ледачий фільтр (`lazy filter`) товарів із низьким запасом (`low stock`).
- **Analytics:** Потокове визначення загальної вартості складу, мінімальної та максимальної ціни.
- **Batch Processing:** Пакетна обробка даних за допомогою `itertools.islice`.
- **Itertools integrations:** Використання `accumulate`, `pairwise`, `groupby` та `islice`.
- **Порівняння Eager vs Lazy:** Вимірювання часу виконання та пікового споживання пам'яті (`tracemalloc`) для великих датасетів (100 000+ записів).

## Структура проєкту
```text
stream_project/
│
├── pyproject.toml
├── README.md
├── data/
│   └── inventory.csv
└── src/
    ├── __init__.py
    ├── main.py
    ├── readers.py
    ├── parsers.py
    ├── models.py
    ├── filters.py
    ├── transformations.py
    ├── batches.py
    ├── analytics.py
    └── pipeline.py
```
## Запуск
```text
python -m src.main
```