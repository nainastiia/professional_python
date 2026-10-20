
"""Unit tests for warehouse services and repository."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.warehouse.models import (
    InsufficientStockError,
    Product,
    WarehouseItem,
)
from src.warehouse.repositories import InMemoryWarehouseRepository
from src.warehouse.services import WarehouseService


def test_repository_add_and_get(product):
    repository = InMemoryWarehouseRepository()
    item = WarehouseItem(product, 4)

    repository.add(item)

    assert repository.get("P001") is item
    assert repository.get("UNKNOWN") is None


def test_repository_rejects_duplicate_code(product):
    repository = InMemoryWarehouseRepository()
    repository.add(WarehouseItem(product, 1))

    with pytest.raises(ValueError, match="already exists"):
        repository.add(WarehouseItem(product, 2))


def test_repository_all_returns_all_items():
    repository = InMemoryWarehouseRepository()
    first = WarehouseItem(Product("A", "First", 10), 1)
    second = WarehouseItem(Product("B", "Second", 20), 2)

    repository.add(first)
    repository.add(second)

    assert repository.all() == [first, second]


def test_register_product(warehouse_service):
    item = warehouse_service.register_product(
        Product("P003", "Monitor", 7000),
        quantity=2,
    )

    assert warehouse_service.find_product("P003") is item
    assert item.quantity == 2


def test_find_product_returns_none_for_unknown_code(warehouse_service):
    assert warehouse_service.find_product("UNKNOWN") is None


def test_receive_updates_stock(warehouse_service):
    item = warehouse_service.receive("P001", 5)
    assert item.quantity == 15


def test_issue_updates_stock(warehouse_service):
    item = warehouse_service.issue("P001", 4)
    assert item.quantity == 6


def test_receive_unknown_product_raises(warehouse_service):
    with pytest.raises(KeyError, match="not found"):
        warehouse_service.receive("UNKNOWN", 1)


def test_issue_unknown_product_raises(warehouse_service):
    with pytest.raises(KeyError, match="not found"):
        warehouse_service.issue("UNKNOWN", 1)


def test_service_issue_insufficient_stock(warehouse_service):
    with pytest.raises(InsufficientStockError):
        warehouse_service.issue("P002", 4)

    assert warehouse_service.find_product("P002").quantity == 3


def test_total_warehouse_value(warehouse_service):
    # P001: 10 * 1250.50; P002: 3 * 500.
    assert warehouse_service.total_value() == pytest.approx(14005.0)


def test_low_stock_uses_configured_threshold(warehouse_service):
    low_stock = warehouse_service.low_stock_items()

    assert [item.product.code for item in low_stock] == ["P002"]


def test_repository_mock_return_value():
    repository = Mock()
    expected_item = WarehouseItem(Product("X", "Test", 10), 2)
    repository.get.return_value = expected_item

    service = WarehouseService(repository, low_stock_threshold=5)

    assert service.find_product("X") is expected_item
    repository.get.assert_called_once_with("X")


def test_repository_mock_side_effect():
    repository = Mock()
    repository.get.side_effect = [
        WarehouseItem(Product("A", "First", 10), 1),
        None,
    ]
    service = WarehouseService(repository, low_stock_threshold=5)

    assert service.find_product("A") is not None
    assert service.find_product("B") is None
    assert repository.get.call_count == 2


def test_service_interacts_with_repository():
    repository = Mock()
    repository.get.return_value = WarehouseItem(
        Product("A", "Test", 10),
        5,
    )
    service = WarehouseService(repository, low_stock_threshold=5)

    service.receive("A", 2)

    repository.get.assert_called_once_with("A")
    assert repository.get.return_value.quantity == 7


def test_invalid_low_stock_threshold_is_rejected():
    with pytest.raises(ValueError, match="threshold"):
        WarehouseService(Mock(), low_stock_threshold=-1)


@pytest.mark.asyncio
async def test_reorder_low_stock_uses_async_mock(warehouse_service):
    provider = Mock()
    provider.reorder = AsyncMock(return_value=True)

    result = await warehouse_service.reorder_low_stock(
        provider,
        reorder_quantity=10,
    )

    assert result == {"P002": True}
    provider.reorder.assert_awaited_once_with("P002", 10)


@pytest.mark.asyncio
async def test_reorder_side_effect_reports_supplier_failure(
    warehouse_service,
):
    provider = Mock()
    provider.reorder = AsyncMock(side_effect=[False])

    result = await warehouse_service.reorder_low_stock(
        provider,
        reorder_quantity=8,
    )

    assert result == {"P002": False}
    provider.reorder.assert_awaited_once_with("P002", 8)


@pytest.mark.asyncio
async def test_reorder_rejects_invalid_quantity(warehouse_service):
    provider = Mock()
    provider.reorder = AsyncMock()

    with pytest.raises(ValueError, match="positive"):
        await warehouse_service.reorder_low_stock(provider, 0)

    provider.reorder.assert_not_awaited()
