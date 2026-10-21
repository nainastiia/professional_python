from reliable_warehouse.exceptions import RecordValidationError
from reliable_warehouse.models import WarehouseItem

ALLOWED_CATEGORIES = {"electronics", "groceries", "stationery", "hardware", "clothing"}

def parse_warehouse_item(row: dict[str, str], *, line_number: int) -> WarehouseItem:
    try:
        code = row.get("code", "").strip()
        if not code:
            raise RecordValidationError("Item code is empty", line_number=line_number, field="code")

        name = row.get("name", "").strip()
        if not name:
            raise RecordValidationError("Item name is empty", line_number=line_number, field="name")

        try:
            quantity = int(row["quantity"])
        except (KeyError, TypeError, ValueError) as error:
            raise RecordValidationError("Invalid quantity", line_number=line_number, field="quantity") from error

        if quantity < 0:
            raise RecordValidationError("Quantity must be greater than or equal to 0", line_number=line_number, field="quantity")

        try:
            price = float(row["price"])
        except (KeyError, TypeError, ValueError) as error:
            raise RecordValidationError("Invalid price", line_number=line_number, field="price") from error

        if price < 0:
            raise RecordValidationError("Price must be greater than or equal to 0", line_number=line_number, field="price")

        category = row.get("category", "").strip().lower()
        if category not in ALLOWED_CATEGORIES:
            raise RecordValidationError(f"Invalid or disallowed category: '{category}'", line_number=line_number, field="category")

        return WarehouseItem(
            code=code,
            name=name,
            quantity=quantity,
            price=price,
            category=category,
        )
    except KeyError as error:
        raise RecordValidationError(f"Missing required field: {error}", line_number=line_number) from error