
"""Unit tests for environment-based configuration."""

import pytest

from src.warehouse.config import (
    DEFAULT_LOW_STOCK_THRESHOLD,
    get_low_stock_threshold,
)


def test_default_low_stock_threshold(monkeypatch):
    monkeypatch.delenv("WAREHOUSE_LOW_STOCK_THRESHOLD", raising=False)

    assert get_low_stock_threshold() == DEFAULT_LOW_STOCK_THRESHOLD


def test_custom_low_stock_threshold(monkeypatch):
    monkeypatch.setenv("WAREHOUSE_LOW_STOCK_THRESHOLD", "12")

    assert get_low_stock_threshold() == 12


def test_invalid_low_stock_threshold(monkeypatch):
    monkeypatch.setenv("WAREHOUSE_LOW_STOCK_THRESHOLD", "abc")

    with pytest.raises(ValueError, match="must be an integer"):
        get_low_stock_threshold()


def test_negative_low_stock_threshold(monkeypatch):
    monkeypatch.setenv("WAREHOUSE_LOW_STOCK_THRESHOLD", "-1")

    with pytest.raises(ValueError, match="cannot be negative"):
        get_low_stock_threshold()
