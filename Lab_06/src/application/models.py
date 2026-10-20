from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class WarehouseItem:
    code: str
    name: str
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("Product code cannot be empty")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Warehouse:
    items: dict[str, WarehouseItem] = field(default_factory=dict)

    def add(self, item: WarehouseItem) -> None:
        if item.code in self.items:
            existing = self.items[item.code]
            self.items[item.code] = WarehouseItem(
                code=existing.code,
                name=existing.name,
                quantity=existing.quantity + item.quantity,
                unit_price=existing.unit_price
            )
        else:
            self.items[item.code] = item

    def receive_stock(self, code: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Received quantity must be positive")
        if code not in self.items:
            raise KeyError(f"Item with code {code} not found")
        item = self.items[code]
        self.items[code] = WarehouseItem(
            code=item.code,
            name=item.name,
            quantity=item.quantity + qty,
            unit_price=item.unit_price
        )

    def ship_stock(self, code: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Shipped quantity must be positive")
        if code not in self.items:
            raise KeyError(f"Item with code {code} not found")
        item = self.items[code]
        if item.quantity < qty:
            raise ValueError("Insufficient stock for shipping")
        self.items[code] = WarehouseItem(
            code=item.code,
            name=item.name,
            quantity=item.quantity - qty,
            unit_price=item.unit_price
        )

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, code: str) -> bool:
        return code in self.items