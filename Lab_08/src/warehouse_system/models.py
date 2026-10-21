from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    min_stock_level = Column(Integer, default=5, nullable=False)

    operations = relationship(
        "StockOperation", back_populates="product", cascade="all, delete-orphan"
    )


class StockOperation(Base):
    __tablename__ = "stock_operations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    operation_type = Column(
        String, nullable=False
    )  # 'incoming' або 'write-off'
    amount = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    product = relationship("Product", back_populates="operations")