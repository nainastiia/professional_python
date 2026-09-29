from dataclasses import dataclass


@dataclass
class WarehouseItem:
    code: str
    name: str
    quantity: int
    price: float

    @property
    def total_value(self) -> float:
        return self.quantity * self.price