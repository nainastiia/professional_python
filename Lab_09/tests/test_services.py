import pytest
from warehouse_system.repositories import WarehouseRepository
from warehouse_system.services import WarehouseService
from warehouse_system.models import WarehouseItemCreate


def test_service_add_and_get():
    repo = WarehouseRepository()
    service = WarehouseService(repo)

    item_data = WarehouseItemCreate(code="P1", name="Item 1", quantity=10, price=100.0)
    service.add_item(item_data)

    retrieved = service.get_item("P1")
    assert retrieved is not None
    assert retrieved.name == "Item 1"


def test_stock_movement():
    repo = WarehouseRepository()
    service = WarehouseService(repo)

    service.add_item(WarehouseItemCreate(code="P1", name="Item 1", quantity=10, price=100.0))
    updated = service.record_movement("P1", -3)
    assert updated.quantity == 7

    with pytest.raises(ValueError):
        service.record_movement("P1", -10)