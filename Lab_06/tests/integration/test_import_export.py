import pytest
from application.exporters import CSVExporter, CSVImporter, JSONExporter


@pytest.mark.integration
def test_csv_export_and_import_integration(tmp_path, sample_item_list):
    file_path = tmp_path / "warehouse.csv"
    CSVExporter.export_to_file(sample_item_list, file_path)
    assert file_path.exists()

    imported = CSVImporter.import_from_file(file_path)
    assert len(imported) == 3
    assert imported[0].code == sample_item_list[0].code
    assert imported[0].unit_price == pytest.approx(sample_item_list[0].unit_price)


@pytest.mark.integration
def test_json_export_integration(tmp_path, sample_item_list):
    json_path = tmp_path / "warehouse.json"
    JSONExporter.export_to_file(sample_item_list, json_path)
    assert json_path.exists()

    content = json_path.read_text(encoding="utf-8")
    assert "Laptop" in content
    assert "P-003" in content


@pytest.mark.integration
def test_import_malformed_csv_raises(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("code,name,quantity\nP-1,Test,10\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed CSV record"):
        CSVImporter.import_from_file(bad_csv)


@pytest.mark.integration
def test_import_malformed_numeric_raises(tmp_path):
    bad_csv = tmp_path / "bad_num.csv"
    bad_csv.write_text("code,name,quantity,unit_price\nP-1,Test,abc,10.0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed numeric record"):
        CSVImporter.import_from_file(bad_csv)