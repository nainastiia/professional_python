from src.warehouse_system.models import WarehouseItem


class InsufficientStockError(Exception):
    """Виняток для випадків, коли списання перевищує наявну кількість товару на складі."""
    pass


def add_stock(item: WarehouseItem, amount: int) -> None:
    """Надходження товару на склад."""
    if amount > 0:
        item.quantity += amount


def remove_stock(item: WarehouseItem, amount: int) -> None:
    """Списання товару зі складу з перевіркою залишку."""
    if amount > item.quantity:
        raise InsufficientStockError(
            f"Неможливо списати {amount} од. товару '{item.name}'. На складі є лише {item.quantity} од."
        )
    item.quantity -= amount


def find_item_by_code(items: list[WarehouseItem], code: str) -> WarehouseItem | None:
    """Пошук позиції за унікальним кодом."""
    for item in items:
        if item.code.lower() == code.lower():
            return item
    return None


def calculate_total_warehouse_value(items: list[WarehouseItem]) -> float:
    """Обчислення загальної вартості всіх позицій на складі."""
    return sum(item.total_value for item in items)


def get_low_stock_items(items: list[WarehouseItem], threshold: int = 5) -> list[WarehouseItem]:
    """Визначення товарів із низьким запасом (менше або дорівнює пороговому значенню)."""
    return [item for item in items if item.quantity <= threshold]