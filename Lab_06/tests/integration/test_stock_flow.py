
"""Integration tests for complete warehouse workflows."""

import io
import json
from unittest.mock import AsyncMock, Mock

import pytest

from src.warehouse.exporters import export_json, stream_csv_import
from src.warehouse.models import Product
from src.warehouse.repositories import InMemoryWarehouseRepository
from src.warehouse.services import WarehouseService


@pytest.mark.integration
def test_complete_stock_flow():
    repository = InMemoryWarehouseRepository()
    service = WarehouseService(repository, low_stock_threshold=3)

    service.register_product(
        Product("P001", "Keyboard", 100),
        quantity=10,
    )

    service.receive("P001", 5)
    service.issue("P001", 4)

    item = service.find_product("P001")

    assert item is not None
    assert item.quantity == 11
    assert service.total_value() == pytest.approx(1100.0)


@pytest.mark.integration
def test_csv_import_to_warehouse_and_json_export(tmp_path):
    csv_source = io.StringIO(
        "code,name,quantity,unit_price\n"
        "P001,Keyboard,5,100\n"
        "P002,Mouse,2,50\n"
    )

    repository = InMemoryWarehouseRepository()

    for item in stream_csv_import(csv_source):
        repository.add(item)

    service = WarehouseService(repository, low_stock_threshold=2)
    output_file = tmp_path / "warehouse.json"

    export_json(repository.all(), output_file)

    exported = json.loads(output_file.read_text(encoding="utf-8"))

    assert service.find_product("P001").quantity == 5
    assert service.find_product("P002").quantity == 2
    assert service.total_value() == pytest.approx(600.0)
    assert [row["code"] for row in exported] == ["P001", "P002"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_low_stock_reorder_workflow():
    repository = InMemoryWarehouseRepository()
    service = WarehouseService(repository, low_stock_threshold=3)

    service.register_product(
        Product("P001", "Keyboard", 100),
        quantity=10,
    )
    service.register_product(
        Product("P002", "Mouse", 50),
        quantity=2,
    )

    provider = Mock()
    provider.reorder = AsyncMock(return_value=True)

    result = await service.reorder_low_stock(provider, reorder_quantity=10)

    assert result == {"P002": True}
    provider.reorder.assert_awaited_once_with("P002", 10)

    # Reordering requests stock from the supplier; it does not
    # automatically change the on-hand quantity.
    assert service.find_product("P002").quantity == 2
