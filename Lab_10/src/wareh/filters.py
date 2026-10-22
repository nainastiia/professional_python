from collections.abc import Iterable, Iterator
from src.models import InventoryRecord


def validate_inventory(rows: Iterable[dict[str, str]]) -> tuple[Iterator[InventoryRecord], dict[str, int]]:
    valid_count = 0
    invalid_count = 0

    def generator():
        nonlocal valid_count, invalid_count
        for row in rows:
            try:
                code = row["code"].strip()
                name = row["name"].strip()
                quantity = int(row["quantity"])
                price = float(row["price"])
                category = row["category"].strip()

                if not code or not name or quantity < 0 or price < 0:
                    invalid_count += 1
                    continue

                valid_count += 1
                yield InventoryRecord(code=code, name=name, quantity=quantity, price=price, category=category)
            except (ValueError, KeyError, TypeError):
                invalid_count += 1
                continue

    return generator(), {"valid": valid_count, "invalid": invalid_count}


def filter_low_stock(records: Iterable[InventoryRecord], threshold: int) -> Iterator[InventoryRecord]:
    for record in records:
        if record.quantity <= threshold:
            yield record