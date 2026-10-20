
"""Shared pytest fixtures."""

import pytest

from warehouse.models import Product, WarehouseItem
from warehouse.repositories import InMemoryWarehouseRepository
from warehouse.services import WarehouseService


@pytest.fixture
def product() -> Product:
    return Product(
        code="P001",
        name="Keyboard",
        unit_price=1250.50,
    )


@pytest.fixture
def warehouse_item(product: Product) -> WarehouseItem:
    return WarehouseItem(product=product, quantity=10)


@pytest.fixture
def repository() -> InMemoryWarehouseRepository:
    return InMemoryWarehouseRepository()


@pytest.fixture
def warehouse_service(
    repository: InMemoryWarehouseRepository,
) -> WarehouseService:
    service = WarehouseService(
        repository=repository,
        low_stock_threshold=5,
    )

    service.register_product(
        Product(code="P001", name="Keyboard", unit_price=1250.50),
        quantity=10,
    )
    service.register_product(
        Product(code="P002", name="Mouse", unit_price=500.00),
        quantity=3,
    )

    return service
