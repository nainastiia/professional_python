import pytest
from warehouse.models import WarehouseItem

def test_creation(item):
    assert (item.code, item.quantity) == ('A1', 10)

def test_value(item):
    assert item.value == pytest.approx(1255)

@pytest.mark.parametrize('quantity', [0, 1, 100])
def test_valid_quantity(quantity):
    assert WarehouseItem('X', 'X', quantity, 1).quantity == quantity

@pytest.mark.parametrize('quantity', [-1, 1.2, True, '2'])
def test_invalid_quantity(quantity):
    with pytest.raises(ValueError, match='quantity'):
        WarehouseItem('X', 'X', quantity, 1)

@pytest.mark.parametrize('price', [0, 0.01, 100.25])
def test_valid_price(price):
    assert WarehouseItem('X', 'X', 0, price).unit_price == pytest.approx(price)

@pytest.mark.parametrize('price', [-1, float('inf'), float('nan'), True, '10'])
def test_invalid_price(price):
    with pytest.raises(ValueError, match='unit_price'):
        WarehouseItem('X', 'X', 0, price)

@pytest.mark.parametrize('code,name', [('', 'ok'), ('A', ''), (None, 'ok')])
def test_required_fields(code, name):
    with pytest.raises(ValueError):
        WarehouseItem(code, name, 1, 2)
