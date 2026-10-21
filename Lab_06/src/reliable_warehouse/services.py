import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from reliable_warehouse.exceptions import RecordValidationError
from reliable_warehouse.models import WarehouseItem
from reliable_warehouse.readers import read_csv_rows
from reliable_warehouse.validators import parse_warehouse_item

logger = logging.getLogger(__name__)


@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0
    low_stock_count: int = 0


def process_warehouse_items(
        path: Path,
        *,
        skip_invalid: bool,
        low_stock_threshold: int,
        statistics: ImportStatistics,
) -> Iterator[WarehouseItem]:
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            item = parse_warehouse_item(row, line_number=line_number)
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning("Invalid record at line %s: %s", error.line_number, error)
            if skip_invalid:
                continue
            raise

        statistics.valid += 1
        if item.quantity <= low_stock_threshold:
            statistics.low_stock_count += 1
            logger.warning("Low stock warning for item '%s' (Code: %s): quantity is %s", item.name, item.code,
                           item.quantity)

        yield item