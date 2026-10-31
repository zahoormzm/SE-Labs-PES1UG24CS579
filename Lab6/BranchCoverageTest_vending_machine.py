"""Branch stage: independently exercise all vending-machine decisions."""

import pytest

from vending_machine import COINS, PRICES, make_change, purchase, select_item


@pytest.mark.parametrize("item,price", list(PRICES.items()))
def test_selection_credit_boundaries(item, price):
    """Exercise below, at and above each item's price."""
    stock = {item: 1}
    assert select_item(item, stock, price - 1) == "insufficient"
    assert select_item(item, stock, price) == "ok"
    assert select_item(item, stock, price + 1) == "ok"
    assert stock == {item: 1}


@pytest.mark.parametrize(
    "item,stock,credit,expected",
    [("water", {}, 0, "invalid"),
     ("cola", {}, 0, "sold_out"),
     ("cola", {"cola": 0}, 500, "sold_out"),
     ("chips", {"chips": 1}, -1, "insufficient")],
)
def test_selection_guard_order(item, stock, credit, expected):
    """Earlier guards determine the result when several conditions fail."""
    original = stock.copy()
    assert select_item(item, stock, credit) == expected
    assert stock == original


@pytest.mark.parametrize("amount", [-1, -5, -100])
def test_negative_change_raises(amount):
    """Cover the previously untested negative-amount exception."""
    with pytest.raises(ValueError, match="^negative amount$"):
        make_change(amount)


@pytest.mark.parametrize(
    "amount,expected",
    [(0, []), (5, [5]), (10, [10]), (25, [25]), (50, [50]), (100, [100]),
     (200, [100, 100]), (190, [100, 50, 25, 10, 5]),
     (240, [100, 100, 25, 10, 5])],
)
def test_exact_change(amount, expected):
    """Cover loop entry, repeated iterations, skipped coins and loop exit."""
    result = make_change(amount)
    assert result == expected
    assert sum(result) == amount
    assert all(coin in COINS for coin in result)


@pytest.mark.parametrize("amount", [1, 4, 6, 24, 26, 101])
def test_unrepresentable_change(amount):
    """A residual amount smaller than the minimum coin is not exact."""
    assert make_change(amount) is None


@pytest.mark.parametrize(
    "item,stock,credit,expected",
    [("water", {"cola": 2}, 200, "invalid"),
     ("cola", {}, 200, "sold_out"),
     ("cola", {"cola": 0}, 200, "sold_out"),
     ("chips", {"chips": 1}, 99, "insufficient"),
     ("cola", {"cola": 2}, 151, "no_exact_change")],
)
def test_purchase_failures_do_not_mutate(item, stock, credit, expected):
    """Cover the non-ok return and the no-exact-change return."""
    original = stock.copy()
    assert purchase(item, stock, credit) == (expected, [])
    assert stock == original


@pytest.mark.parametrize("item,price", list(PRICES.items()))
@pytest.mark.parametrize("extra,expected_change", [(0, []), (190, [100, 50, 25, 10, 5])])
def test_purchase_success(item, price, extra, expected_change):
    """Cover successful zero-change and nonzero-change purchases."""
    stock = dict.fromkeys(PRICES, 2)
    original = stock.copy()
    assert purchase(item, stock, price + extra) == ("dispensed", expected_change)
    assert stock[item] == 1
    assert all(stock[key] == original[key] for key in PRICES if key != item)
    assert sum(expected_change) == extra


def test_final_item_then_sold_out():
    """Verify the stock transition across two calls on the same dictionary."""
    stock = {"candy": 1}
    assert purchase("candy", stock, 75) == ("dispensed", [])
    assert stock == {"candy": 0}
    assert purchase("candy", stock, 75) == ("sold_out", [])
    assert stock == {"candy": 0}
