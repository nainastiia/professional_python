import csv
import random
import tracemalloc
import time
from pathlib import Path
from itertools import islice, chain, accumulate, pairwise, groupby
from src.pipeline import build_pipeline
from src.batches import batched_inventory
from src.analytics import calculate_inventory_analytics
from src.readers import read_lines
from src.parsers import parse_csv_rows
from src.filters import validate_inventory

def generate_test_file(path: Path, count: int) -> None:
    categories = ["Electronics", "Tools", "Office", "Home", "Garden"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["code", "name", "quantity", "price", "category"])
        for i in range(1, count + 1):
            writer.writerow([
                f"PRD-{i:05d}",
                f"Item {i}",
                random.randint(-2, 50),  # Деякі будуть від'ємними для тестування валідації
                round(random.uniform(5.0, 2500.0), 2),
                random.choice(categories)
            ])


def measure_peak_memory(func, *args):
    tracemalloc.start()
    start_time = time.perf_counter()
    result = func(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = time.perf_counter() - start_time
    return result, peak, elapsed


def main():
    data_path = Path("data/inventory.csv")
    record_count = 100_000

    print(f"Генерація тестового файлу на {record_count} записів...")
    generate_test_file(data_path, record_count)

    operations = {"PRD-00001": 10, "PRD-00002": -5}

    # 1. Демонстрація роботи Pipeline та Analytics
    print("\n[1] Запуск Lazy Pipeline та агрегації:")
    pipeline, stats = build_pipeline(data_path, operations, low_stock_threshold=5)
    analytics = calculate_inventory_analytics(pipeline)
    print(f"Статистика валідації: Коректних = {stats['valid']}, Некоректних = {stats['invalid']}")
    print(f"Загальна вартість складу: {analytics['total_warehouse_value']:,.2f} грн")
    print(f"Мінімальна ціна: {analytics['min_price']} | Максимальна ціна: {analytics['max_price']}")

    # 2. Використання islice для пошуку перших N позицій
    print("\n[2] Перші 3 товари з низьким запасом (islice):")
    pipeline, _ = build_pipeline(data_path, operations, low_stock_threshold=5)
    for item in islice(pipeline, 3):
        print(item)

    # 3. Використання itertools (accumulate, pairwise, groupby)
    print("\n[3] Демонстрація itertools (accumulate / pairwise / chain):")
    sample_prices = [100.0, 150.0, 130.0, 200.0, 220.0]
    print("Accumulate (накопичення цін):", list(accumulate(sample_prices)))
    print("Pairwise (різниці сусідніх цін):", [curr - prev for prev, curr in pairwise(sample_prices)])

    # 4. Batch Processing
    print("\n[4] Демонстрація Batch Processing (розмір пакета = 2):")
    pipeline, _ = build_pipeline(data_path, operations, low_stock_threshold=2)
    for batch in islice(batched_inventory(pipeline, 2), 2):
        print(f"Батч із {len(batch)} елементів:", [b.code for b in batch])

    # 5. Порівняння Eager та Lazy підходів (Пам'ять та Час)
    print("\n[5] Порівняння Eager vs Lazy на 100 000 записах:")

    def eager_processing(path: Path):
        with path.open("r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            # Матеріалізація всього списку в пам'яті
            valid = [r for r in reader if float(r["price"]) >= 0 and int(r["quantity"]) >= 0]
            return len(valid)

    def lazy_processing(path: Path):
        lines = read_lines(path)
        rows = parse_csv_rows(lines)
        valid, _ = validate_inventory(rows)
        return sum(1 for _ in valid)

    _, eager_mem, eager_time = measure_peak_memory(eager_processing, data_path)
    _, lazy_mem, lazy_time = measure_peak_memory(lazy_processing, data_path)

    print(f"Eager approach -> Час: {eager_time:.4f} с | Пік пам'яті: {eager_mem / 1024 / 1024:.2f} MB")
    print(f"Lazy approach  -> Час: {lazy_time:.4f} с | Пік пам'яті: {lazy_mem / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()