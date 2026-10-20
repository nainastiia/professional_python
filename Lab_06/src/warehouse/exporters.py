
"""CSV import and JSON export utilities."""

import csv
import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TextIO

from src.warehouse.models import Product, WarehouseItem


class WarehouseValidationError(ValueError):
    """Raised when an imported warehouse record is malformed."""


def stream_csv_import(
    source: str | Path | TextIO,
) -> Iterator[WarehouseItem]:
    """
    Stream warehouse positions from CSV.

    Expected header:
        code,name,quantity,unit_price
    """
    should_close = False

    if isinstance(source, (str, Path)):
        handle = open(source, "r", encoding="utf-8-sig", newline="")
        should_close = True
    else:
        handle = source

    try:
        reader = csv.DictReader(handle)
        expected_fields = {"code", "name", "quantity", "unit_price"}

        if reader.fieldnames is None:
            raise WarehouseValidationError("CSV file is empty.")

        if not expected_fields.issubset(set(reader.fieldnames)):
            raise WarehouseValidationError(
                "CSV must contain code,name,quantity,unit_price columns."
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                code = row["code"]
                name = row["name"]
                quantity_text = row["quantity"]
                price_text = row["unit_price"]

                if None in (code, name, quantity_text, price_text):
                    raise ValueError("Missing field.")

                product = Product(
                    code=code.strip(),
                    name=name.strip(),
                    unit_price=float(price_text),
                )
                quantity = int(quantity_text)

                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")

                yield WarehouseItem(product=product, quantity=quantity)

            except (TypeError, ValueError, KeyError) as exc:
                raise WarehouseValidationError(
                    f"Invalid CSV record at line {line_number}: {exc}"
                ) from exc
    finally:
        if should_close:
            handle.close()


def export_json(
    items: Iterable[WarehouseItem],
    destination: str | Path | TextIO,
) -> None:
    """Write warehouse stock positions as JSON."""
    payload = [
        {
            "code": item.product.code,
            "name": item.product.name,
            "quantity": item.quantity,
            "unit_price": item.product.unit_price,
            "stock_value": item.stock_value,
        }
        for item in items
    ]

    if hasattr(destination, "write"):
        json.dump(payload, destination, ensure_ascii=False, indent=2)
        destination.write("\n")
        return

    path = Path(destination)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
