from sqlalchemy import func, select
from sqlalchemy.orm import Session
from warehouse_system.models import Product, StockOperation

class InsufficientStockError(Exception):
    """Виняток для випадків, коли списання перевищує наявну кількість товару на складі."""
    pass

class WarehouseService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def calculate_total_warehouse_value(self) -> float:
        statement = select(func.sum(Product.quantity * Product.price))
        result = self.session.scalar(statement)
        return float(result) if result else 0.0

    def get_low_stock_items(self, threshold: int = 5) -> list[Product]:
        statement = select(Product).where(Product.quantity <= threshold)
        return list(self.session.scalars(statement))

    def process_stock_operation(self, product_id: int, operation_type: str, qty: int) -> Product:
        """
        Транзакційна операція надходження (IN) або списання (OUT).
        Забороняє списання понад залишок та виконує rollback при помилці[cite: 25].
        """
        try:
            product = self.session.get(Product, product_id)
            if product is None:
                raise ValueError("Product not found")

            if operation_type == "IN":
                product.quantity += qty
            elif operation_type == "OUT":
                if product.quantity < qty:
                    raise InsufficientStockError(
                        f"Неможливо списати {qty} од. товару '{product.name}'. На складі є лише {product.quantity} од."
                    )
                product.quantity -= qty
            else:
                raise ValueError("Invalid operation type")

            # Логування операції в історії
            operation = StockOperation(
                product_id=product.id,
                operation_type=operation_type,
                quantity=qty
            )
            self.session.add(operation)
            self.session.commit()
            self.session.refresh(product)
            return product
        except Exception:
            self.session.rollback()
            raise