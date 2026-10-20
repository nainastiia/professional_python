
"""Domain models and validation for warehouse stock."""

from dataclasses import dataclass
import math


class InsufficientStockError(Exception):
    """Raised when an issue operation exceeds available stock."""


def _validate_quantity(quantity: int) -> None:
    """Quantity must be a non-negative integer, excluding bool."""
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")


def _validate_positive_quantity(quantity: int) -> None:
    """Operations must move at least one item."""
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")


@dataclass(frozen=True)
class Product:
    """A product identified by a unique stock code."""

    code: str
    name: str
    unit_price: float

    def __post_init__(self) -> None:
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("Product code cannot be empty.")

        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Product name cannot be empty.")

        if isinstance(self.unit_price, bool):
            raise ValueError("Unit price must be a number.")

        if not isinstance(self.unit_price, (int, float)):
            raise ValueError("Unit price must be a number.")

        if not math.isfinite(self.unit_price):
            raise ValueError("Unit price must be finite.")

        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        # Normalize integer prices to float.
        object.__setattr__(self, "unit_price", float(self.unit_price))


@dataclass
class WarehouseItem:
    """A product and its current quantity in the warehouse."""

    product: Product
    quantity: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.product, Product):
            raise TypeError("product must be a Product instance.")

        _validate_quantity(self.quantity)

    @property
    def stock_value(self) -> float:
        """Return the total monetary value of this stock position."""
        return self.product.unit_price * self.quantity

    def receive(self, quantity: int) -> None:
        """Add stock to the warehouse."""
        _validate_positive_quantity(quantity)
        self.quantity += quantity

    def issue(self, quantity: int) -> None:
        """Remove stock or raise an exception if stock is insufficient."""
        _validate_positive_quantity(quantity)

        if quantity > self.quantity:
            raise InsufficientStockError(
                f"Cannot issue {quantity} units of "
                f"{self.product.code}; available: {self.quantity}."
            )

        self.quantity -= quantity
