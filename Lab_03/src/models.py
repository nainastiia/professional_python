from typing import NamedTuple

class InventoryRecord(NamedTuple):
    code: str
    name: str
    quantity: int
    price: float
    category: str