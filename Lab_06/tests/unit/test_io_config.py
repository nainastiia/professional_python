import json
import pytest
from warehouse.io import read_items, export_json
from warehouse.config import low_stock_threshold
from warehouse.models import ImportRecordError

def test_config_default(monkeypatch):
    monkeypatch.delenv('WAREHOUSE_LOW_STOCK', raising=False)
    assert low_stock_threshold() == 5

def test_config_override(monkeypatch):
    monkeypatch.setenv('WAREHOUSE_LOW_STOCK', '2')
    assert low_stock_threshold() == 2

@pytest.mark.parametrize('raw', ['abc', '-1'])
def test_config_invalid(monkeypatch, raw):
    monkeypatch.setenv('WAREHOUSE_LOW_STOCK', raw)
    with pytest.raises(ValueError):
        low_stock_threshold()

def test_bad_quantity(csv_factory):
    path = csv_factory('code,name,quantity,unit_price\nA1,Test,wrong,2\n')
    with pytest.raises(ImportRecordError) as exc:
        list(read_items(path))
    assert exc.value.field == 'quantity'
    assert isinstance(exc.value.__cause__, ValueError)

def test_bad_header(csv_factory):
    with pytest.raises(ImportRecordError, match='header'):
        list(read_items(csv_factory('code,name\nA1,Test\n')))

def test_export(tmp_path, item):
    path = tmp_path / 'result.json'
    export_json([item], path)
    assert json.loads(path.read_text(encoding='utf-8'))[0]['value'] == pytest.approx(1255)
