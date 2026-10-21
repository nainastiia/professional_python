import pytest
from warehouse_system.models import Product
from warehouse_system.repositories import ProductRepository
from warehouse_system.services import WarehouseService, InsufficientStockError


def test_crud_product(session) -> None:
    repo = ProductRepository(session)

    # Create
    product = Product(code="A-01", name="Монітор 27\"", quantity=4, price=8500.0)
    saved = repo.add(product)
    assert saved.id is not None
    assert saved.code == "A-01"

    # Read
    loaded = repo.get_by_id(saved.id)
    assert loaded is not None
    assert loaded.name == "Монітор 27\""

    # Update
    loaded.price = 9000.0
    updated = repo.update(loaded)
    assert updated.price == 9000.0

    # Delete
    result = repo.delete(saved.id)
    assert result is True
    assert repo.get_by_id(saved.id) is None


def test_incoming_and_writeoff(session) -> None:
    repo = ProductRepository(session)
    service = WarehouseService(session)

    product = repo.add(Product(code="A-02", name="Клавіатура", quantity=10, price=2200.0))

    # Надходження
    service.process_stock_operation(product.id, "IN", 5)
    assert product.quantity == 15

    # Списання
    service.process_stock_operation(product.id, "OUT", 3)
    assert product.quantity == 12


def test_insufficient_stock_rollback(session) -> None:
    repo = ProductRepository(session)
    service = WarehouseService(session)

    product = repo.add(Product(code="A-03", name="Миша", quantity=2, price=1200.0))

    # Спроба списати більше, ніж є — має викликати виняток та rollback (кількість не змінюється)[cite: 25]
    with pytest.raises(InsufficientStockError):
        service.process_stock_operation(product.id, "OUT", 5)

    session.refresh(product)
    assert product.quantity == 2


def test_warehouse_aggregations(session) -> None:
    repo = ProductRepository(session)
    service = WarehouseService(session)

    repo.add(Product(code="A-1", name="Item 1", quantity=10, price=100.0))
    repo.add(Product(code="A-2", name="Item 2", quantity=2, price=500.0))

    # Загальна вартість: (10 * 100) + (2 * 500) = 1000 + 1000 = 2000
    total = service.calculate_total_warehouse_value()
    assert total == 2000.0