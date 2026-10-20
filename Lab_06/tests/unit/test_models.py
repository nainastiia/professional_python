import pytest
from application.models import WarehouseItem, Warehouse

def test_warehouse_item_creation(sample_item):
    assert sample_item.code == "P-001"
    assert sample_item.name == "Laptop"
    assert sample_item.total_price == 125000.0

def test_warehouse_container_operations(sample_warehouse, sample_item):
    assert len(sample_warehouse) == 1
    assert "P-001" in sample_warehouse
    assert "P-999" not in sample_warehouse

def test_receive_and_ship_stock(sample_item):
    wh = Warehouse()
    wh.add(sample_item)
    wh.receive_stock("P-001", 5)
    assert wh.items["P-001"].quantity == 10

    wh.ship_stock("P-001", 4)
    assert wh.items["P-001"].quantity == 6

def test_insufficient_stock_raises(sample_item):
    wh = Warehouse()
    wh.add(sample_item)
    with pytest.raises(ValueError, match="Insufficient stock"):
        wh.ship_stock("P-001", 20)

def test_invalid_stock_operations(sample_item):
    wh = Warehouse()
    wh.add(sample_item)
    with pytest.raises(ValueError, match="positive"):
        wh.receive_stock("P-001", 0)
    with pytest.raises(KeyError):
        wh.receive_stock("UNKNOWN", 5)
    with pytest.raises(ValueError, match="positive"):
        wh.ship_stock("P-001", -2)
    with pytest.raises(KeyError):
        wh.ship_stock("UNKNOWN", 5)