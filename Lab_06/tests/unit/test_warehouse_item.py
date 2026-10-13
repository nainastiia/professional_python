import pytest
from warehouse.models import WarehouseItem
from warehouse.value_objects import Money
from warehouse.exceptions import InsufficientStockError

def test_item_receive(sample_item):
    sample_item.receive(5)
    assert sample_item.quantity == 20

def test_item_issue(sample_item):
    sample_item.issue(5)
    assert sample_item.quantity == 10

def test_item_issue_insufficient_stock(sample_item):
    with pytest.raises(InsufficientStockError) as exc_info:
        sample_item.issue(20)
    assert exc_info.value.available == 15
    assert exc_info.value.requested == 20

@pytest.mark.parametrize("invalid_qty", [-1, 0])
def test_invalid_receive_amount(sample_item, invalid_qty):
    with pytest.raises(ValueError):
        sample_item.receive(invalid_qty)