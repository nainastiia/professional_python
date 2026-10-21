from warehouse_system.database import SessionLocal, engine
from warehouse_system.models import Base, Product
from warehouse_system.repositories import ProductRepository
from warehouse_system.services import WarehouseService

def main() -> None:
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        product_repo = ProductRepository(session)
        service = WarehouseService(session)

        # Додавання тестового товару, якщо він відсутній
        existing = product_repo.get_by_code("PRD-001")
        if not existing:
            p = Product(code="PRD-001", name="Laptop Pro", quantity=10, price=1200.0, minimum_stock=3)
            product_repo.add(p)

        print("--- Warehouse Products ---")
        for prod in product_repo.get_all():
            print(f"Code: {prod.code} | Name: {prod.name} | Qty: {prod.quantity} | Price: {prod.price}")

        total_val = service.calculate_total_warehouse_value()
        print(f"\nTotal Warehouse Value: ${total_val:.2f}")

        # Демонстрація транзакції (успішне надходження)
        prod = product_repo.get_by_code("PRD-001")
        if prod:
            service.process_stock_operation(prod.id, "IN", 5)
            print(f"After IN operation, quantity: {prod.quantity}")

if __name__ == "__main__":
    main()