import pytest
from unittest.mock import Mock
from warehouse.services import WarehouseService
from warehouse.exporters import export_inventory_json
from warehouse.exceptions import MalformedRecordError


def test_csv_import_and_export_pipeline(tmp_path):
    csv_file = tmp_path / "stock_input.csv"
    csv_file.write_text(
        "code,name,quantity,unit_price\n"
        "PRD-100,Keyboard,10,1200.0\n"
        "PRD-101,Monitor,5,7500.0\n",
        encoding="utf-8"
    )

    repo = Mock()
    supplier = Mock()
    service = WarehouseService(repo, supplier)

    items = list(service.stream_import_csv(csv_file))
    assert len(items) == 2
    assert items[0].name == "Keyboard"

    output_json = tmp_path / "report.json"
    export_inventory_json(items, output_json)

    assert output_json.exists()


def test_csv_import_malformed_record(tmp_path):
    csv_file = tmp_path / "bad_stock.csv"
    csv_file.write_text(
        "code,name,quantity,unit_price\n"
        "PRD-100,Keyboard,invalid_qty,1200.0\n",
        encoding="utf-8"
    )
    repo = Mock()
    supplier = Mock()
    service = WarehouseService(repo, supplier)

    with pytest.raises(MalformedRecordError):
        list(service.stream_import_csv(csv_file))