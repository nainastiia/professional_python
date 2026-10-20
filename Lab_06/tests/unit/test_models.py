from application.models import WarehouseItem, Warehouse

def test_warehouse_item_creation(sample_item):
    assert sample_item.code == "P-001"
    assert sample_item.name == "Laptop"
    assert sample_item.total_price == 125000.0

def test_warehouse_container_operations(sample_warehouse, sample_item):
    assert len(sample_warehouse) == 1
    assert "P-001" in sample_warehouse
    assert "P-999" not in sample_warehouse