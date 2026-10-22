from sqlalchemy import select
from sqlalchemy.orm import Session
from warehouse_system.models import Product, StockOperation

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_by_code(self, code: str) -> Product | None:
        statement = select(Product).where(Product.code == code)
        return self.session.scalar(statement)

    def get_all(self) -> list[Product]:
        statement = select(Product)
        return list(self.session.scalars(statement))

    def update(self, product: Product) -> Product:
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False
        self.session.delete(product)
        self.session.commit()
        return True


class StockOperationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, operation: StockOperation) -> StockOperation:
        self.session.add(operation)
        self.session.commit()
        self.session.refresh(operation)
        return operation

    def get_by_product(self, product_id: int) -> list[StockOperation]:
        statement = select(StockOperation).where(StockOperation.product_id == product_id)
        return list(self.session.scalars(statement))