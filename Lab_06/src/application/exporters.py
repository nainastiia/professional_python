import csv
import json
from pathlib import Path
from typing import List
from application.models import WarehouseItem

class CSVExporter:
    @staticmethod
    def export_to_file(items: List[WarehouseItem], file_path: Path) -> None:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["code", "name", "quantity", "unit_price"])
            for i in items:
                writer.writerow([i.code, i.name, i.quantity, i.unit_price])

class CSVImporter:
    @staticmethod
    def import_from_file(file_path: Path) -> List[WarehouseItem]:
        items: List[WarehouseItem] = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not all(k in row for k in ("code", "name", "quantity", "unit_price")):
                    raise ValueError("Malformed CSV record: missing columns")
                # перевірка на валідність числових полів (malformed quantity record)
                try:
                    qty = int(row["quantity"])
                    price = float(row["unit_price"])
                except ValueError as err:
                    raise ValueError("Malformed numeric record in CSV") from err

                item = WarehouseItem(
                    code=row["code"],
                    name=row["name"],
                    quantity=qty,
                    unit_price=price,
                )
                items.append(item)
        return items

class JSONExporter:
    @staticmethod
    def export_to_file(items: List[WarehouseItem], file_path: Path) -> None:
        data = [
            {"code": i.code, "name": i.name, "quantity": i.quantity, "unit_price": i.unit_price}
            for i in items
        ]
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")