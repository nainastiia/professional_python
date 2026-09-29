from collections.abc import Iterable, Iterator
from src.models import InventoryRecord

def process_stock_operations(records: Iterable[InventoryRecord], operations: dict[str, int]) -> Iterator[InventoryRecord]:
    for record in records:
        delta = operations.get(record.code, 0)
        new_qty = record.quantity + delta
        if new_qty < 0:
            new_qty = 0
        yield record._replace(quantity=new_qty)