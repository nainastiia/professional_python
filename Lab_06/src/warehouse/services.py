
"""Warehouse business logic and reorder integration."""

from typing import Protocol

from src.warehouse.config import get_low_stock_threshold
from src.warehouse.models import Product, WarehouseItem
from src.warehouse.repositories import WarehouseRepository


class ReorderProvider(Protocol):
    """Interface for an external supplier/reorder service."""

    async def reorder(self, product_code: str, quantity: int) -> bool:
        ...


class WarehouseService:
    """Coordinate warehouse operations using a repository."""

    def __init__(
        self,
        repository: WarehouseRepository,
        low_stock_threshold: int | None = None,
    ) -> None:
        if low_stock_threshold is None:
            low_stock_threshold = get_low_stock_threshold()

        if (
            isinstance(low_stock_threshold, bool)
            or not isinstance(low_stock_threshold, int)
            or low_stock_threshold < 0
        ):
            raise ValueError(
                "Low-stock threshold must be a non-negative integer."
            )

        self.repository = repository
        self.low_stock_threshold = low_stock_threshold

    def register_product(
        self,
        product: Product,
        quantity: int = 0,
    ) -> WarehouseItem:
        """Register a product and its initial stock."""
        item = WarehouseItem(product=product, quantity=quantity)
        self.repository.add(item)
        return item

    def find_product(self, product_code: str) -> WarehouseItem | None:
        """Find a stock position by product code."""
        return self.repository.get(product_code)

    def receive(self, product_code: str, quantity: int) -> WarehouseItem:
        """Receive stock for an existing product."""
        item = self.repository.get(product_code)

        if item is None:
            raise KeyError(f"Product {product_code} was not found.")

        item.receive(quantity)
        return item

    def issue(self, product_code: str, quantity: int) -> WarehouseItem:
        """Issue stock for an existing product."""
        item = self.repository.get(product_code)

        if item is None:
            raise KeyError(f"Product {product_code} was not found.")

        item.issue(quantity)
        return item

    def total_value(self) -> float:
        """Return the combined value of all warehouse stock."""
        return sum(item.stock_value for item in self.repository.all())

    def low_stock_items(self) -> list[WarehouseItem]:
        """Return positions at or below the configured threshold."""
        return [
            item
            for item in self.repository.all()
            if item.quantity <= self.low_stock_threshold
        ]

    async def reorder_low_stock(
        self,
        provider: ReorderProvider,
        reorder_quantity: int = 10,
    ) -> dict[str, bool]:
        """Ask a provider to reorder every low-stock product."""
        if (
            isinstance(reorder_quantity, bool)
            or not isinstance(reorder_quantity, int)
            or reorder_quantity <= 0
        ):
            raise ValueError("Reorder quantity must be a positive integer.")

        results: dict[str, bool] = {}

        for item in self.low_stock_items():
            results[item.product.code] = await provider.reorder(
                item.product.code,
                reorder_quantity,
            )

        return results
