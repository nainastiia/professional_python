
"""Unit tests for Product and WarehouseItem."""

import math

import pytest

from warehouse.models import (
    InsufficientStockError,
    Product,
    WarehouseItem,
)


def test_product_creation(product):
    assert product.code == "P001"
    assert product.name == "Keyboard"
    assert product.unit_price == pytest.approx(1250.50)


def test_product_accepts_zero_price():
    product = Product("FREE", "Promotional item", 0)
    assert product.unit_price == 0.0


@pytest.mark.parametrize("code", ["", " ", "\t"])
def test_product_rejects_empty_code(code):
    with pytest.raises(ValueError, match="code"):
        Product(code, "Keyboard", 100)


@pytest.mark.parametrize("name", ["", " ", "\n"])
def test_product_rejects_empty_name(name):
    with pytest.raises(ValueError, match="name"):
        Product("P001", name, 100)


@pytest.mark.parametrize("price", [-1, -0.01, float("-inf"), float("inf"), math.nan])
def test_product_rejects_invalid_price(price):
    with pytest.raises(ValueError):
        Product("P001", "Keyboard", price)


@pytest.mark.parametrize("price", ["100", None, True])
def test_product_rejects_non_numeric_price(price):
    with pytest.raises(ValueError, match="number"):
        Product("P001", "Keyboard", price)


def test_warehouse_item_creation(warehouse_item):
    assert warehouse_item.quantity == 10
    assert warehouse_item.product.code == "P001"


@pytest.mark.parametrize("quantity", [-1, -10])
def test_warehouse_item_rejects_negative_quantity(product, quantity):
    with pytest.raises(ValueError, match="negative"):
        WarehouseItem(product, quantity)


@pytest.mark.parametrize("quantity", [1.5, "5", True, None])
def test_warehouse_item_rejects_non_integer_quantity(product, quantity):
    with pytest.raises(ValueError, match="integer"):
        WarehouseItem(product, quantity)


def test_stock_value_uses_quantity_and_unit_price(warehouse_item):
    assert warehouse_item.stock_value == pytest.approx(12505.0)


def test_receive_increases_quantity(warehouse_item):
    warehouse_item.receive(5)
    assert warehouse_item.quantity == 15


def test_issue_decreases_quantity(warehouse_item):
    warehouse_item.issue(4)
    assert warehouse_item.quantity == 6


def test_issue_exact_available_quantity(warehouse_item):
    warehouse_item.issue(10)
    assert warehouse_item.quantity == 0


def test_issue_more_than_available_raises(warehouse_item):
    with pytest.raises(InsufficientStockError, match="available"):
        warehouse_item.issue(11)

    # A failed issue must not modify stock.
    assert warehouse_item.quantity == 10


@pytest.mark.parametrize("quantity", [0, -1, -5])
def test_receive_rejects_non_positive_quantity(warehouse_item, quantity):
    with pytest.raises(ValueError, match="greater than zero"):
        warehouse_item.receive(quantity)


@pytest.mark.parametrize("quantity", [0, -1, 1.2, True, "2"])
def test_issue_rejects_invalid_quantity(warehouse_item, quantity):
    with pytest.raises(ValueError):
        warehouse_item.issue(quantity)
