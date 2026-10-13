class WarehouseError(Exception):
    """Базовий виняток системи обліку складу."""
    pass

class InsufficientStockError(WarehouseError):
    """Виняток при нестачі товару на складі."""
    def __init__(self, message: str, available: int, requested: int) -> None:
        super().__init__(message)
        self.available = available
        self.requested = requested

class MalformedRecordError(WarehouseError):
    """Виняток для пошкоджених/некоректних записів у файлі."""
    pass