import json
from pathlib import Path
from typing import List
from warehouse.models import WarehouseItem

def export_inventory_json(items: List[WarehouseItem], path: Path) -> None:
    data = [
        {
            "code": item.product_code,
            "name": item.name,
            "quantity": item.quantity,
            "unit_price": item.unit_price.amount,
            "currency": item.unit_price.currency
        }
        for item in items
    ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")