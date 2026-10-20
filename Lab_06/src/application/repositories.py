from typing import Generic, TypeVar, Dict, List, Optional

T = TypeVar("T")

class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self._storage: Dict[str, T] = {}

    def add(self, key: str, item: T) -> None:
        self._storage[key] = item

    def get_by_key(self, key: str) -> Optional[T]:
        return self._storage.get(key)

    def list_all(self) -> List[T]:
        return list(self._storage.values())