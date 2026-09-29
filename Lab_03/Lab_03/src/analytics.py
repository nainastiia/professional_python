from collections.abc import Iterable
from src.models import InventoryRecord


def calculate_inventory_analytics(records: Iterable[InventoryRecord]) -> dict:
    total_value = 0.0
    total_items = 0
    min_price = None
    max_price = None

    for record in records:
        item_val = record.quantity * record.price
        total_value += item_val
        total_items += record.quantity

        if min_price is None or record.price < min_price:
            min_price = record.price
        if max_price is None or record.price > max_price:
            max_price = record.price

    return {
        "total_warehouse_value": total_value,
        "total_items_count": total_items,
        "min_price": min_price if min_price is not None else 0.0,
        "max_price": max_price if max_price is not None else 0.0
    }