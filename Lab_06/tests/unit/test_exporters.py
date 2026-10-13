import json
from warehouse.exporters import export_inventory_json


def test_json_export(tmp_path, inventory_list):
    output_file = tmp_path / "inventory.json"
    export_inventory_json(inventory_list, output_file)

    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["code"] == "PRD-001"
    assert data[0]["quantity"] == 15