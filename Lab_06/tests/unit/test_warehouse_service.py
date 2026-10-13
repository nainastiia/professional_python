import pytest
from unittest.mock import Mock, AsyncMock
from warehouse.services import WarehouseService, get_low_stock_threshold
from warehouse.models import WarehouseItem
from warehouse.value_objects import Money
from warehouse.exceptions import InsufficientStockError


def test_total_inventory_value(inventory_list):
    repo = Mock()
    supplier = Mock()
    service = WarehouseService(repo, supplier)

    total = service.calculate_total_inventory_value(inventory_list)
    # 15 * 25000 + 3 * 500 = 375000 + 1500 = 376500
    assert total.amount == pytest.approx(376500.0)


def test_empty_inventory_value():
    repo = Mock()
    supplier = Mock()
    service = WarehouseService(repo, supplier)
    assert service.calculate_total_inventory_value([]).amount == 0.0


def test_low_stock_filtering(inventory_list):
    repo = Mock()
    supplier = Mock()
    service = WarehouseService(repo, supplier)

    low_items = service.get_low_stock_items(inventory_list)
    assert len(low_items) == 1
    assert low_items[0].product_code == "PRD-002"


def test_checkout_insufficient_stock_side_effect(sample_item):
    repo = Mock()
    repo.get_by_code.return_value = sample_item

    supplier = Mock()
    supplier.reorder.return_value = "ORDER-999"

    service = WarehouseService(repo, supplier)

    with pytest.raises(InsufficientStockError):
        service.process_issuing("PRD-001", 100)

    # Перевірка interaction та side_effect
    supplier.reorder.assert_called_once_with("PRD-001", 100)
    repo.save.assert_not_called()


def test_configuration_monkeypatch(monkeypatch):
    monkeypatch.setenv("LOW_STOCK_THRESHOLD", "25")
    assert get_low_stock_threshold() == 25


def test_configuration_default(monkeypatch):
    monkeypatch.delenv("LOW_STOCK_THRESHOLD", raising=False)
    assert get_low_stock_threshold() == 10


def test_process_incoming_product_not_found():
    repo = Mock()
    repo.get_by_code.return_value = None  # Товар не знайдено
    supplier = Mock()
    service = WarehouseService(repo, supplier)

    with pytest.raises(ValueError, match="not found"):
        service.process_incoming("UNKNOWN-001", 10)


def test_process_issuing_product_not_found():
    repo = Mock()
    repo.get_by_code.return_value = None  # Товар не знайдено
    supplier = Mock()
    service = WarehouseService(repo, supplier)

    with pytest.raises(ValueError, match="not found"):
        service.process_issuing("UNKNOWN-001", 5)
        
@pytest.mark.asyncio
async def test_async_reorder_provider():
    provider = AsyncMock()
    provider.async_reorder.return_value = {"status": "success", "order_id": "ORD-123"}

    result = await provider.async_reorder("PRD-001", 50)
    assert result["status"] == "success"
    provider.async_reorder.assert_awaited_once_with("PRD-001", 50)