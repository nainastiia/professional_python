from unittest.mock import Mock, AsyncMock
import asyncio
import pytest
from warehouse.services import Warehouse
from warehouse.models import InsufficientStockError

def test_empty_warehouse():
    assert Warehouse().total_value() == 0

def test_find(warehouse, item):
    assert warehouse.find('A1') is item

def test_find_missing(warehouse):
    assert warehouse.find('missing') is None

def test_receive(warehouse):
    assert warehouse.receive('A1', 3) == 13

def test_issue(warehouse):
    assert warehouse.issue('A1', 10) == 0

def test_insufficient_stock(warehouse):
    with pytest.raises(InsufficientStockError, match='insufficient'):
        warehouse.issue('A1', 11)
    assert warehouse.find('A1').quantity == 10

@pytest.mark.parametrize('amount', [0, -1, 2.5, True])
def test_invalid_amount(warehouse, amount):
    with pytest.raises(ValueError):
        warehouse.receive('A1', amount)

def test_missing_code(warehouse):
    with pytest.raises(KeyError):
        warehouse.issue('absent', 1)

def test_low_stock(warehouse):
    assert warehouse.low_stock(9) == []
    assert [x.code for x in warehouse.low_stock(10)] == ['A1']

def test_invalid_threshold(warehouse):
    with pytest.raises(ValueError):
        warehouse.low_stock(-1)

def test_duplicate(warehouse, item_factory):
    with pytest.raises(ValueError, match='duplicate'):
        warehouse.add(item_factory('A1'))

def test_repository_interaction(item):
    repo = Mock()
    warehouse = Warehouse(repo)
    warehouse.add(item)
    repo.save.assert_called_once_with(item)

def test_supplier_return_value(warehouse):
    supplier = Mock()
    supplier.reorder.return_value = 'REQ-1'
    assert warehouse.request_reorder('A1', supplier) == 'REQ-1'
    supplier.reorder.assert_called_once_with('A1', 10)

def test_supplier_side_effect(warehouse):
    supplier = Mock()
    supplier.reorder.side_effect = ConnectionError('offline')
    with pytest.raises(ConnectionError, match='offline'):
        warehouse.request_reorder('A1', supplier)

def test_async_reorder(warehouse):
    provider = Mock()
    provider.reorder = AsyncMock(return_value='ASYNC-1')
    assert asyncio.run(warehouse.async_reorder('A1', provider)) == 'ASYNC-1'
    provider.reorder.assert_awaited_once_with('A1', 10)
