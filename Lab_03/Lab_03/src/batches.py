from collections.abc import Iterable, Iterator
from itertools import islice
from src.models import InventoryRecord

def batched_inventory(iterable: Iterable[InventoryRecord], size: int) -> Iterator[list[InventoryRecord]]:
    iterator = iter(iterable)
    while True:
        batch = list(islice(iterator, size))
        if not batch:
            break
        yield batch