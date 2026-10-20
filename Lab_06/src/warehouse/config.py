
"""Configuration helpers for the warehouse application."""

import os


DEFAULT_LOW_STOCK_THRESHOLD = 5


def get_low_stock_threshold() -> int:
    """Read the low-stock threshold from the environment."""
    raw_value = os.getenv(
        "WAREHOUSE_LOW_STOCK_THRESHOLD",
        str(DEFAULT_LOW_STOCK_THRESHOLD),
    )

    try:
        threshold = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "WAREHOUSE_LOW_STOCK_THRESHOLD must be an integer."
        ) from exc

    if threshold < 0:
        raise ValueError("Low-stock threshold cannot be negative.")

    return threshold
