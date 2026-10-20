
"""Unit tests for CSV import and JSON export."""

import io
import json

import pytest

from src.warehouse.exporters import (
    WarehouseValidationError,
    export_json,
    stream_csv_import,
)
from src.warehouse.models import Product, WarehouseItem


def test_csv_import_from_file_object():
    source = io.StringIO(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,10,1250.5\n"
        "P002,Mouse,3,500\n"
    )

    items = list(stream_csv_import(source))

    assert len(items) == 2
    assert items[0].product.code == "P001"
    assert items[0].quantity == 10
    assert items[0].product.unit_price == pytest.approx(1250.5)
    assert items[1].product.name == "Mouse"


def test_csv_import_streams_records():
    source = io.StringIO(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,10,1250.5\n"
    )

    result = stream_csv_import(source)

    # The importer returns an iterator rather than a complete list.
    assert iter(result) is result
    assert next(result).product.code == "P001"


def test_csv_import_from_path(tmp_path):
    csv_file = tmp_path / "stock.csv"
    csv_file.write_text(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,7,100\n",
        encoding="utf-8",
    )

    items = list(stream_csv_import(csv_file))

    assert len(items) == 1
    assert items[0].quantity == 7


def test_csv_import_rejects_missing_columns():
    source = io.StringIO("code,name\nP001,Keyboard\n")

    with pytest.raises(WarehouseValidationError, match="must contain"):
        list(stream_csv_import(source))


def test_csv_import_rejects_invalid_quantity():
    source = io.StringIO(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,not-a-number,100\n"
    )

    with pytest.raises(WarehouseValidationError, match="line 2"):
        list(stream_csv_import(source))


def test_csv_import_rejects_negative_quantity():
    source = io.StringIO(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,-1,100\n"
    )

    with pytest.raises(WarehouseValidationError, match="line 2"):
        list(stream_csv_import(source))


def test_csv_import_rejects_invalid_price():
    source = io.StringIO(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,5,invalid\n"
    )

    with pytest.raises(WarehouseValidationError, match="line 2"):
        list(stream_csv_import(source))


def test_csv_import_rejects_empty_file():
    source = io.StringIO("")

    with pytest.raises(WarehouseValidationError, match="empty"):
        list(stream_csv_import(source))


def test_json_export_to_path(tmp_path):
    items = [
        WarehouseItem(Product("P001", "Keyboard", 100), 3),
        WarehouseItem(Product("P002", "Mouse", 50), 2),
    ]
    output_file = tmp_path / "stock.json"

    export_json(items, output_file)

    data = json.loads(output_file.read_text(encoding="utf-8"))

    assert len(data) == 2
    assert data[0]["code"] == "P001"
    assert data[0]["quantity"] == 3
    assert data[0]["stock_value"] == pytest.approx(300.0)


def test_json_export_to_file_object():
    items = [WarehouseItem(Product("P001", "Keyboard", 100), 2)]
    destination = io.StringIO()

    export_json(items, destination)

    data = json.loads(destination.getvalue())

    assert data[0]["name"] == "Keyboard"
    assert data[0]["stock_value"] == pytest.approx(200.0)


def test_json_export_empty_list(tmp_path):
    output_file = tmp_path / "empty.json"

    export_json([], output_file)

    assert json.loads(output_file.read_text(encoding="utf-8")) == []
