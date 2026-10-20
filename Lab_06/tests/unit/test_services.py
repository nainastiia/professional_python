import pytest
from unittest.mock import Mock, AsyncMock
from application.services import (
    find_by_code,
    calculate_total_inventory_value,
    get_low_stock_items,
    AsyncReorderService,
)


def test_find_by_code(sample_item_list):
    found = find_by_code(sample_item_list, "P-002")
    assert found is not None
    assert found.name == "Mouse"
    assert find_by_code(sample_item_list, "UNKNOWN") is None


def test_calculate_total_inventory_value(sample_item_list):
    total = calculate_total_inventory_value(sample_item_list)
    # 5*25000 + 2*500 + 10*1200 = 125000 + 1000 + 12000 = 138000
    assert total == pytest.approx(138000.0)


def test_get_low_stock_items(sample_item_list):
    # threshold = 6 -> Laptop (5) and Mouse (2) are low stock
    low = get_low_stock_items(sample_item_list, threshold=6)
    assert len(low) == 2
    assert low[0].code == "P-001"
    assert low[1].code == "P-002"


def test_mock_supplier_notification():
    mock_supplier = Mock()
    mock_supplier.reorder.return_value = "ORD-999"

    result = mock_supplier.reorder("P-001", 10)
    assert result == "ORD-999"
    mock_supplier.reorder.assert_called_once_with("P-001", 10)


def test_mock_supplier_side_effect():
    mock_supplier = Mock()
    mock_supplier.reorder.side_effect = ConnectionError("Supplier timeout")

    with pytest.raises(ConnectionError, match="Supplier timeout"):
        mock_supplier.reorder("P-001", 10)


@pytest.mark.asyncio
async def test_async_reorder_service():
    mock_client = AsyncMock()
    mock_client.place_order.return_value = {"status": "success"}

    service = AsyncReorderService(async_client=mock_client)
    result = await service.check_and_reorder_async("P-001", 10, 3)

    assert result == "success"
    mock_client.place_order.assert_awaited_once_with("P-001", 7)