import json
from collections.abc import Iterable
from pathlib import Path
from reliable_warehouse.exceptions import DataExportError
from reliable_warehouse.models import WarehouseItem

def export_items_json(students: Iterable[WarehouseItem], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    count = 0
    try:
        with temporary.open("w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for item in students:
                if not first:
                    file.write(",\n")
                json.dump(item.to_dict(), file, ensure_ascii=False, indent=2)
                first = False
                count += 1
            file.write("\n]\n")
        temporary.replace(path)
    except (OSError, TypeError) as error:
        temporary.unlink(missing_ok=True)
        raise DataExportError(f"Cannot export data to {path}") from error
    return count