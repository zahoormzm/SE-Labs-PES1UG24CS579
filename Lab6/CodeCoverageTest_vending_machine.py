"""Line-coverage stage: selection, change and purchase outcomes."""

import pytest

from vending_machine import make_change, purchase, select_item


@pytest.mark.parametrize(
    "item,stock,credit,expected",
    [
        ("water", {}, 200, "invalid"),
        ("cola", {}, 200, "sold_out"),
        ("chips", {"chips": 0}, 100, "sold_out"),
        ("candy", {"candy": 1}, 74, "insufficient"),
        ("cola", {"cola": 1}, 150, "ok"),
        ("chips", {"chips": 2}, 200, "ok"),
    ],
)
def test_selection(item, stock, credit, expected):
    """Check each selection status without consuming stock."""
    original = stock.copy()
    assert select_item(item, stock, credit) == expected
    assert stock == original


@pytest.mark.parametrize(
    "amount,expected",
    [(0, []), (185, [100, 50, 25, 10]), (190, [100, 50, 25, 10, 5]),
     (6, None), (4, None)],
)
def test_change(amount, expected):
    """Check zero, exact coin combinations and impossible remainders."""
    assert make_change(amount) == expected


@pytest.mark.parametrize(
    "item,stock,credit,expected",
    [
        ("water", {"cola": 1}, 200, ("invalid", [])),
        ("cola", {"cola": 0}, 200, ("sold_out", [])),
        ("candy", {"candy": 1}, 70, ("insufficient", [])),
        ("cola", {"cola": 2}, 151, ("no_exact_change", [])),
    ],
)
def test_failed_purchase_preserves_stock(item, stock, credit, expected):
    """Every failure leaves the original inventory intact."""
    original = stock.copy()
    assert purchase(item, stock, credit) == expected
    assert stock == original


@pytest.mark.parametrize(
    "credit,expected_change",
    [(150, []), (200, [50]), (340, [100, 50, 25, 10, 5])],
)
def test_purchase_dispenses_once(credit, expected_change):
    """Successful purchase decrements only the selected item."""
    stock = {"cola": 2, "chips": 3}
    assert purchase("cola", stock, credit) == ("dispensed", expected_change)
    assert stock == {"cola": 1, "chips": 3}
    assert sum(expected_change) == credit - 150
