from sqlalchemy import select
from sqlalchemy.orm import Session
from warehouse_system.models import Product, StockOperation


class ProductRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Product]:
        statement = select(Product).order_by(Product.name)
        return list(self.session.scalars(statement))

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        statement = select(Product).where(Product.sku == sku)
        return self.session.scalar(statement)

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()

    def get_low_stock(self) -> list[Product]:
        statement = select(Product).where(
            Product.quantity <= Product.min_stock_level
        )
        return list(self.session.scalars(statement))


class StockOperationRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, operation: StockOperation) -> StockOperation:
        self.session.add(operation)
        self.session.commit()
        self.session.refresh(operation)
        return operation

    def get_all(self) -> list[StockOperation]:
        statement = select(StockOperation).order_by(StockOperation.id.desc())
        return list(self.session.scalars(statement))