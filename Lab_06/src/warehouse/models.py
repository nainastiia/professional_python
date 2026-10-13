from dataclasses import dataclass
from warehouse.value_objects import Money

@dataclass
class WarehouseItem:
    product_code: str
    name: str
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

    def receive(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Receive amount must be positive")
        self.quantity += amount

    def issue(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Issue amount must be positive")
        from warehouse.exceptions import InsufficientStockError
        if self.quantity < amount:
            raise InsufficientStockError(
                f"Insufficient stock for {self.product_code}",
                available=self.quantity,
                requested=amount
            )
        self.quantity -= amount

    @property
    def total_value(self) -> Money:
        return Money(self.unit_price.amount * self.quantity, self.unit_price.currency)