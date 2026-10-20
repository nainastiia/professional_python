
"""Repository abstractions and an in-memory implementation."""

from typing import Protocol

from warehouse.models import Product, WarehouseItem


class WarehouseRepository(Protocol):
    """Interface expected by the warehouse service."""

    def add(self, item: WarehouseItem) -> None:
        ...

    def get(self, product_code: str) -> WarehouseItem | None:
        ...

    def all(self) -> list[WarehouseItem]:
        ...


class InMemoryWarehouseRepository:
    """Store warehouse items in memory, indexed by product code."""

    def __init__(self) -> None:
        self._items: dict[str, WarehouseItem] = {}

    def add(self, item: WarehouseItem) -> None:
        if not isinstance(item, WarehouseItem):
            raise TypeError("item must be a WarehouseItem instance.")

        code = item.product.code

        if code in self._items:
            raise ValueError(f"Product {code} already exists.")

        self._items[code] = item

    def get(self, product_code: str) -> WarehouseItem | None:
        return self._items.get(product_code)

    def all(self) -> list[WarehouseItem]:
        return list(self._items.values())

    def register_product(
        self,
        product: Product,
        quantity: int = 0,
    ) -> WarehouseItem:
        """Create and store a new warehouse position."""
        item = WarehouseItem(product=product, quantity=quantity)
        self.add(item)
        return item
