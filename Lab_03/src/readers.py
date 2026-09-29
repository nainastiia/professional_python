from pathlib import Path
from collections.abc import Iterator

def read_lines(path: Path) -> Iterator[str]:
    with path.open("r", encoding="utf-8") as file:
        yield from file