from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class WarehouseItem:
    code: str
    name: str
    quantity: int
    price: float
    category: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    low_stock_threshold: int
    skip_invalid: bool

@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path

@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig