from sqlalchemy.orm import Session
from warehouse_system.models import Product, StockOperation
from warehouse_system.repositories import (
    ProductRepository,
    StockOperationRepository,
)
from warehouse_system.schemas import (
    ProductCreate,
    ProductUpdate,
    StockOperationCreate,
)


class WarehouseService:

    def __init__(self, session: Session) -> None:
        self.session = session
        self.product_repo = ProductRepository(session)
        self.operation_repo = StockOperationRepository(session)

    def list_products(self) -> list[Product]:
        return self.product_repo.get_all()

    def get_product(self, product_id: int) -> Product | None:
        return self.product_repo.get_by_id(product_id)

    def create_product(self, data: ProductCreate) -> Product:
        existing = self.product_repo.get_by_sku(data.sku)
        if existing:
            raise ValueError(
                f"Product with SKU '{data.sku}' already exists."
            )

        product = Product(
            name=data.name,
            sku=data.sku,
            price=data.price,
            quantity=data.quantity,
            min_stock_level=data.min_stock_level,
        )
        return self.product_repo.add(product)

    def update_product(
        self, product_id: int, data: ProductUpdate
    ) -> Product | None:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return None

        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(product, field, value)

        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return False
        self.product_repo.delete(product)
        return True

    def process_incoming(
        self, product_id: int, data: StockOperationCreate
    ) -> StockOperation:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise KeyError("Product not found")

        product.quantity += data.amount
        operation = StockOperation(
            product_id=product.id,
            operation_type="incoming",
            amount=data.amount,
            comment=data.comment,
        )
        return self.operation_repo.add(operation)

    def process_write_off(
        self, product_id: int, data: StockOperationCreate
    ) -> StockOperation:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise KeyError("Product not found")

        # Перевірка умови з Варіанта 10: не дозволяти списання понад залишок
        if product.quantity < data.amount:
            raise ValueError("Write-off amount exceeds available stock.")

        product.quantity -= data.amount
        operation = StockOperation(
            product_id=product.id,
            operation_type="write-off",
            amount=data.amount,
            comment=data.comment,
        )
        return self.operation_repo.add(operation)

    def get_low_stock(self) -> list[Product]:
        return self.product_repo.get_low_stock()

    def get_operations(self) -> list[StockOperation]:
        return self.operation_repo.get_all()

    def get_total_value(self) -> dict[str, float | int]:
        products = self.product_repo.get_all()
        total_val = sum(p.price * p.quantity for p in products)
        return {
            "total_stock_value": round(total_val, 2),
            "total_products_count": len(products),
        }