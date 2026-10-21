from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from warehouse_system.database import engine, get_session
from warehouse_system.external_api import check_multiple_products_stock
from warehouse_system.models import (  # <--- Імпортуємо Base з models, а не з database
    Base,
    Product,
    StockOperation,
)
from warehouse_system.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    StockOperationCreate,
    StockOperationResponse,
    WarehouseValueResponse,
)
from warehouse_system.services import WarehouseService

# Створення таблиць БД при старті
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Warehouse Management System API",
    version="1.0.0",
    description="REST API для системи обліку складських запасів (Варіант 10)",
)
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from warehouse_system.database import get_session
from warehouse_system.external_api import check_multiple_products_stock
from warehouse_system.models import (
    Product,
    StockOperation,
)
from warehouse_system.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    StockOperationCreate,
    StockOperationResponse,
    WarehouseValueResponse,
)
from warehouse_system.services import WarehouseService

app = FastAPI(
    title="Warehouse Management System API",
    version="1.0.0",
    description="REST API для системи обліку складських запасів (Варіант 10)",
)


@app.get("/products", response_model=list[ProductResponse])
async def get_products(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.list_products()


@app.get("/products/low-stock", response_model=list[ProductResponse])
async def get_low_stock_products(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.get_low_stock()


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    service = WarehouseService(session)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data: ProductCreate, session: Session = Depends(get_session)
):
    service = WarehouseService(session)
    try:
        return service.create_product(data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@app.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
):
    service = WarehouseService(session)
    updated = service.update_product(product_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, session: Session = Depends(get_session)
):
    service = WarehouseService(session)
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@app.post(
    "/products/{product_id}/incoming", response_model=StockOperationResponse
)
async def product_incoming(
    product_id: int,
    data: StockOperationCreate,
    session: Session = Depends(get_session),
):
    service = WarehouseService(session)
    try:
        return service.process_incoming(product_id, data)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@app.post(
    "/products/{product_id}/write-off", response_model=StockOperationResponse
)
async def product_write_off(
    product_id: int,
    data: StockOperationCreate,
    session: Session = Depends(get_session),
):
    service = WarehouseService(session)
    try:
        return service.process_write_off(product_id, data)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@app.get("/stock/operations", response_model=list[StockOperationResponse])
async def get_stock_operations(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.get_operations()


@app.get("/stock/value", response_model=WarehouseValueResponse)
async def get_warehouse_value(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.get_total_value()


@app.post("/stock/batch-check")
async def batch_check_stock(product_ids: list[int]):
    """Асинхронний ендпоінт для пакетної перевірки залишків."""
    results = await check_multiple_products_stock(
        "http://127.0.0.1:8000", product_ids
    )
    return {"results": results}

@app.get("/products", response_model=list[ProductResponse])
async def get_products(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.list_products()


@app.get("/products/low-stock", response_model=list[ProductResponse])
async def get_low_stock_products(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.get_low_stock()


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    service = WarehouseService(session)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data: ProductCreate, session: Session = Depends(get_session)
):
    service = WarehouseService(session)
    try:
        return service.create_product(data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@app.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
):
    service = WarehouseService(session)
    updated = service.update_product(product_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, session: Session = Depends(get_session)
):
    service = WarehouseService(session)
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@app.post(
    "/products/{product_id}/incoming", response_model=StockOperationResponse
)
async def product_incoming(
    product_id: int,
    data: StockOperationCreate,
    session: Session = Depends(get_session),
):
    service = WarehouseService(session)
    try:
        return service.process_incoming(product_id, data)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@app.post(
    "/products/{product_id}/write-off", response_model=StockOperationResponse
)
async def product_write_off(
    product_id: int,
    data: StockOperationCreate,
    session: Session = Depends(get_session),
):
    service = WarehouseService(session)
    try:
        return service.process_write_off(product_id, data)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@app.get("/stock/operations", response_model=list[StockOperationResponse])
async def get_stock_operations(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.get_operations()


@app.get("/stock/value", response_model=WarehouseValueResponse)
async def get_warehouse_value(session: Session = Depends(get_session)):
    service = WarehouseService(session)
    return service.get_total_value()


@app.post("/stock/batch-check")
async def batch_check_stock(product_ids: list[int]):
    """Асинхронний ендпоінт для пакетної перевірки залишків."""
    results = await check_multiple_products_stock(
        "http://127.0.0.1:8000", product_ids
    )
    return {"results": results}