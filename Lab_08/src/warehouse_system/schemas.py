from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    sku: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    min_stock_level: int = Field(ge=0, default=5)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    sku: str | None = Field(default=None, min_length=2, max_length=50)
    price: float | None = Field(default=None, gt=0)
    min_stock_level: int | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    quantity: int
    min_stock_level: int

    model_config = {"from_attributes": True}


class StockOperationCreate(BaseModel):
    amount: int = Field(gt=0)
    comment: str | None = None


class StockOperationResponse(BaseModel):
    id: int
    product_id: int
    operation_type: str
    amount: int
    comment: str | None

    model_config = {"from_attributes": True}


class WarehouseValueResponse(BaseModel):
    total_stock_value: float
    total_products_count: int