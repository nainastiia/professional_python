import pytest
from application.models import WarehouseItem

@pytest.mark.parametrize("quantity", [0, 10, 100])
def test_valid_quantities(quantity):
    item = WarehouseItem(code="T-1", name="Test", quantity=quantity, unit_price=10.0)
    assert item.quantity == quantity

@pytest.mark.parametrize("invalid_price", [-1.0, -100.5])
def test_invalid_price_raises_error(invalid_price):
    with pytest.raises(ValueError, match="negative"):
        WarehouseItem(code="T-1", name="Test", quantity=5, unit_price=invalid_price)

def test_invalid_empty_code_raises_error():
    with pytest.raises(ValueError, match="code cannot be empty"):
        WarehouseItem(code="   ", name="Test", quantity=5, unit_price=10.0)

def test_invalid_empty_name_raises_error():
    with pytest.raises(ValueError, match="name cannot be empty"):
        WarehouseItem(code="T-1", name="   ", quantity=5, unit_price=10.0)