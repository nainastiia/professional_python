from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Поле після міграції (Варіант 10)
    minimum_stock: Mapped[int | None] = mapped_column(Integer, nullable=True, default=5)

    operations: Mapped[list["StockOperation"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    @property
    def total_value(self) -> float:
        return self.quantity * self.price


class StockOperation(Base):
    __tablename__ = "stock_operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    operation_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "IN" або "OUT"
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    product: Mapped["Product"] = relationship(back_populates="operations")