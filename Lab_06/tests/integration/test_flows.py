import json
import pytest
from warehouse.io import read_items, export_json
from warehouse.services import Warehouse
from warehouse.config import low_stock_threshold

@pytest.mark.integration
def test_import_to_stock_to_export(csv_factory, tmp_path):
    path = csv_factory('code,name,quantity,unit_price\nA1,Keyboard,3,100\nB2,Mouse,1,50\n')
    warehouse = Warehouse()
    for item in read_items(path):
        warehouse.add(item)
    warehouse.receive('A1', 2)
    warehouse.issue('B2', 1)
    output = tmp_path / 'warehouse.json'
    export_json(warehouse.items.values(), output)
    data = json.loads(output.read_text(encoding='utf-8'))
    assert len(data) == 2
    assert sum(x['value'] for x in data) == pytest.approx(500)

@pytest.mark.integration
def test_config_and_low_stock(csv_factory, monkeypatch):
    monkeypatch.setenv('WAREHOUSE_LOW_STOCK', '3')
    warehouse = Warehouse()
    for item in read_items(csv_factory('code,name,quantity,unit_price\nA1,Keyboard,3,100\nB2,Mouse,4,50\n')):
        warehouse.add(item)
    assert [x.code for x in warehouse.low_stock(low_stock_threshold())] == ['A1']

@pytest.mark.integration
def test_import_error_preserves_existing_stock(csv_factory, item):
    warehouse = Warehouse()
    warehouse.add(item)
    from warehouse.models import ImportRecordError
    with pytest.raises(ImportRecordError):
        for record in read_items(csv_factory('code,name,quantity,unit_price\nX,Invalid,not_int,5\n')):
            warehouse.add(record)
    assert warehouse.total_value() == pytest.approx(1255)
