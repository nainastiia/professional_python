from Lab_01.src.warehouse_system.models import WarehouseItem
from Lab_01.src.warehouse_system.services import (
    add_stock,
    calculate_total_warehouse_value,
    find_item_by_code,
    get_low_stock_items,
    remove_stock,
    InsufficientStockError,
)


def create_demo_items() -> list[WarehouseItem]:
    return [
        WarehouseItem(code="A-01", name="Монітор 27\"", quantity=4, price=8500.0),
        WarehouseItem(code="A-02", name="Клавіатура механічна", quantity=15, price=2200.0),
        WarehouseItem(code="A-03", name="Миша бездротова", quantity=2, price=1200.0),
        WarehouseItem(code="A-04", name="Кабель HDMI 2m", quantity=30, price=350.0),
    ]


def print_items(items: list[WarehouseItem])  -> None:
    print("\n{:<8} | {:<25} | {:<10} | {:<10} | {:<12}".format("Код", "Назва", "Кількість", "Ціна (грн)", "Сума (грн)"))
    print("-" * 75)
    for item in items:
        print(f"{item.code:<8} | {item.name:<25} | {item.quantity:<10} | {item.price:<10.2f} | {item.total_value:<12.2f}")


def print_menu() -> None:
    print("\n--- СИСТЕМА ОБЛІКУ СКЛАДСЬКИХ ЗАПАСІВ ---")
    print("1. Переглянути всі товари")
    print("2. Надходження товару")
    print("3. Списання товару")
    print("4. Загальна вартість складу")
    print("5. Товари з низьким запасом (<= 5 шт.)")
    print("6. Пошук товару за кодом")
    print("0. Вихід")


def main() -> None:
    items = create_demo_items()

    while True:
        print_menu()
        choice = input("Виберіть опцію: ").strip()

        if choice == "1":
            print_items(items)

        elif choice == "2":
            code = input("Введіть код товару: ").strip()
            item = find_item_by_code(items, code)
            if item:
                try:
                    amount = int(input("Кількість для надходження: "))
                    if amount <= 0:
                        print("Помилка: кількість має бути більше нуля.")
                        continue
                    add_stock(item, amount)
                    print(f"Успішно! Новий запас товару '{item.name}': {item.quantity} од.")
                except ValueError:
                    print("Помилка: введіть ціле число.")
            else:
                print("Товар із таким кодом не знайдено.")

        elif choice == "3":
            code = input("Введіть код товару: ").strip()
            item = find_item_by_code(items, code)
            if item:
                try:
                    amount = int(input("Кількість для списання: "))
                    if amount <= 0:
                        print("Помилка: кількість має бути більше нуля.")
                        continue
                    remove_stock(item, amount)
                    print(f"Успішно! Залишок товару '{item.name}': {item.quantity} од.")
                except ValueError:
                    print("Помилка: введіть ціле число.")
                except InsufficientStockError as e:
                    print(f"Помилка списання: {e}")
            else:
                print("Товар із таким кодом не знайдено.")

        elif choice == "4":
            total_val = calculate_total_warehouse_value(items)
            print(f"\nЗагальна вартість усіх товарів на складі: {total_val:,.2f} грн")

        elif choice == "5":
            low_stock = get_low_stock_items(items, threshold=5)
            if low_stock:
                print("\nУвага! Товари з критично низьким запасом:")
                print_items(low_stock)
            else:
                print("\nТоварів із низьким запасом немає.")

        elif choice == "6":
            code = input("Введіть код для пошуку: ").strip()
            item = find_item_by_code(items, code)
            if item:
                print_items([item])
            else:
                print("Товар не знайдено.")

        elif choice == "0":
            print("Роботу програми завершено. До побачення!")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()