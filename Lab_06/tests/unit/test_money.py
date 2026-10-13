import pytest
from warehouse.value_objects import Money

def test_money_creation():
    m = Money(100.0, "UAH")
    assert m.amount == 100.0
    assert m.currency == "UAH"

def test_negative_money_raises():
    with pytest.raises(ValueError, match="negative"):
        Money(-10.0)

@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        (0.0, 0.0),
        (0.01, 0.01),
        (100.50, 100.50),
    ]
)
def test_valid_money_amounts(amount, expected):
    m = Money(amount)
    assert m.amount == pytest.approx(expected)

def test_money_addition():
    m1 = Money(100.0)
    m2 = Money(50.0)
    assert m1 + m2 == Money(150.0)