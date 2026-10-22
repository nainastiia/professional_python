import sqlite3

def find_products_by_code_db_api(database_path: str, code_query: str) -> list[tuple]:
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT code, name, quantity, price 
            FROM products 
            WHERE code LIKE ?
            """,
            (f"%{code_query}%",)
        )
        return cursor.fetchall()