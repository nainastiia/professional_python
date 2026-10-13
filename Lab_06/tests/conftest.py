import pytest
from warehouse.models import WarehouseItem
from warehouse.value_objects import Money

@pytest.fixture
def sample_item() -> WarehouseItem:
    return WarehouseItem(
        product_code="PRD-001",
        name="Laptop",
        quantity=15,
        unit_price=Money(25000.0)
    )

@pytest.fixture
def low_stock_item() -> WarehouseItem:
    return WarehouseItem(
        product_code="PRD-002",
        name="Mouse",
        quantity=3,
        unit_price=Money(500.0)
    )

@pytest.fixture
def inventory_list(sample_item, low_stock_item) -> list[WarehouseItem]:
    return [sample_item, low_stock_item]