import pytest
from application.models import WarehouseItem, Warehouse

@pytest.fixture
def sample_item() -> WarehouseItem:
    return WarehouseItem(code="P-001", name="Laptop", quantity=5, unit_price=25000.0)

@pytest.fixture
def sample_item_list() -> list[WarehouseItem]:
    return [
        WarehouseItem(code="P-001", name="Laptop", quantity=5, unit_price=25000.0),
        WarehouseItem(code="P-002", name="Mouse", quantity=2, unit_price=500.0),
        WarehouseItem(code="P-003", name="Keyboard", quantity=10, unit_price=1200.0),
    ]

@pytest.fixture
def sample_warehouse(sample_item) -> Warehouse:
    wh = Warehouse()
    wh.add(sample_item)
    return wh