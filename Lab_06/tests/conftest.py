import pytest
from warehouse.models import WarehouseItem
from warehouse.services import Warehouse

@pytest.fixture
def item():
    return WarehouseItem('A1', 'Keyboard', 10, 125.5)

@pytest.fixture
def warehouse(item):
    result = Warehouse()
    result.add(item)
    return result

@pytest.fixture
def item_factory():
    def create(code='X', quantity=5, price=10):
        return WarehouseItem(code, 'Sample', quantity, price)
    return create

@pytest.fixture
def csv_factory(tmp_path):
    def create(content):
        path = tmp_path / 'items.csv'
        path.write_text(content, encoding='utf-8')
        return path
    yield create
