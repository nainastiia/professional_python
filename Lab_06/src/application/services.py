import asyncio
from typing import List, Optional
from application.models import WarehouseItem

def add_item(warehouse_items: List[WarehouseItem], item: WarehouseItem) -> List[WarehouseItem]:
    warehouse_items.append(item)
    return warehouse_items

def find_by_code(warehouse_items: List[WarehouseItem], code: str) -> Optional[WarehouseItem]:
    for item in warehouse_items:
        if item.code == code:
            return item
    return None

def calculate_total_inventory_value(warehouse_items: List[WarehouseItem]) -> float:
    return sum(item.total_price for item in warehouse_items)

def get_low_stock_items(warehouse_items: List[WarehouseItem], threshold: int) -> List[WarehouseItem]:
    return [item for item in warehouse_items if item.quantity < threshold]

class AsyncReorderService:
    def __init__(self, async_client) -> None:
        self._client = async_client

    async def check_and_reorder_async(self, code: str, threshold: int, current_qty: int) -> str:
        await asyncio.sleep(0.01)
        if current_qty < threshold:
            response = await self._client.place_order(code, threshold - current_qty)
            return response.get("status", "pending")
        return "sufficient"