import os
import csv
from pathlib import Path
from typing import List, Iterator
from warehouse.models import WarehouseItem
from warehouse.value_objects import Money
from warehouse.exceptions import MalformedRecordError, InsufficientStockError
from warehouse.protocols import WarehouseRepository, SupplierService

def get_low_stock_threshold() -> int:
    return int(os.getenv("LOW_STOCK_THRESHOLD", "10"))

class WarehouseService:
    def __init__(self, repository: WarehouseRepository, supplier: SupplierService) -> None:
        self._repo = repository
        self._supplier = supplier

    def process_incoming(self, code: str, qty: int) -> None:
        item = self._repo.get_by_code(code)
        if not item:
            raise ValueError(f"Product {code} not found")
        item.receive(qty)
        self._repo.save(item)

    def process_issuing(self, code: str, qty: int) -> None:
        item = self._repo.get_by_code(code)
        if not item:
            raise ValueError(f"Product {code} not found")
        try:
            item.issue(qty)
        except InsufficientStockError:
            # Спроба автоматичного перезамовлення через постачальника
            self._supplier.reorder(code, qty)
            raise
        self._repo.save(item)

    def get_low_stock_items(self, items: List[WarehouseItem]) -> List[WarehouseItem]:
        threshold = get_low_stock_threshold()
        return [item for item in items if item.quantity <= threshold]

    def calculate_total_inventory_value(self, items: List[WarehouseItem]) -> Money:
        if not items:
            return Money(0.0)
        total = sum(item.total_value.amount for item in items)
        return Money(total, items[0].unit_price.currency)

    def stream_import_csv(self, file_path: Path) -> Iterator[WarehouseItem]:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    code = row["code"]
                    name = row["name"]
                    qty = int(row["quantity"])
                    price = float(row["unit_price"])
                    yield WarehouseItem(code, name, qty, Money(price))
                except (KeyError, ValueError) as e:
                    raise MalformedRecordError(f"Invalid CSV record: {row}") from e