from pathlib import Path
from src.readers import read_lines
from src.parsers import parse_csv_rows
from src.filters import validate_inventory, filter_low_stock
from src.transformations import process_stock_operations

def build_pipeline(path: Path, operations: dict[str, int], low_stock_threshold: int):
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid_records, stats = validate_inventory(rows)
    updated_records = process_stock_operations(valid_records, operations)
    filtered = filter_low_stock(updated_records, low_stock_threshold)
    return filtered, stats