"""Property and regression tests for Lab 7 vending-machine inputs."""

import string

import pytest
from hypothesis import given, settings, strategies as st

from vending_machine import change_due, parse_coins, slot_position


INPUTS = st.one_of(
    st.text(max_size=50),
    st.none(),
    st.booleans(),
    st.integers(),
    st.binary(max_size=12),
    st.lists(st.integers(), max_size=3),
)
FUZZ = settings(max_examples=150, derandomize=True, report_multiple_bugs=False)
POSITIVE = st.integers(min_value=1, max_value=10_000)
NONNEGATIVE = st.integers(min_value=0, max_value=10_000)
ROW = st.sampled_from(string.ascii_letters)


@FUZZ
@given(INPUTS)
def test_parse_coins_arbitrary(raw):
    result = parse_coins(raw)
    if result is not None:
        assert isinstance(raw, str)
        assert isinstance(result, list) and result
        assert all(type(coin) is int and coin > 0 for coin in result)
        assert result == [int(token) for token in raw.split(",")]


@FUZZ
@given(INPUTS)
def test_slot_position_arbitrary(raw):
    result = slot_position(raw)
    if result is not None:
        assert isinstance(raw, str)
        assert isinstance(result, tuple) and len(result) == 2
        row, column = result
        assert type(row) is int and 0 <= row < 26
        assert type(column) is int and column >= 0
        code = raw.strip()
        assert string.ascii_uppercase[row] == code[0].upper()
        assert column + 1 == int(code[1:])


@FUZZ
@given(INPUTS)
def test_change_due_arbitrary(raw):
    result = change_due(raw)
    if result is not None:
        assert isinstance(raw, str)
        paid, price = (int(token) for token in raw.split("/"))
        count, label = result.split()
        assert label == "five-coins"
        assert paid >= price >= 0 and int(count) >= 0
        assert 5 * int(count) == paid - price


@FUZZ
@given(st.lists(POSITIVE, min_size=1, max_size=12))
def test_valid_coins_round_trip(values):
    raw = " , ".join(str(value) for value in values)
    assert parse_coins(raw) == values


@FUZZ
@given(ROW, POSITIVE)
def test_valid_slot_maps_to_zero_based_coordinates(letter, column):
    code = f" {letter}{column:05} "
    expected_row = string.ascii_uppercase.index(letter.upper())
    assert slot_position(code) == (expected_row, column - 1)


@FUZZ
@given(NONNEGATIVE, NONNEGATIVE)
def test_exact_change_conserves_value(price, coins):
    paid = price + 5 * coins
    assert change_due(f" {paid} / {price} ") == f"{coins} five-coins"


@FUZZ
@given(NONNEGATIVE, POSITIVE)
def test_underpayment_is_rejected(paid, shortfall):
    assert change_due(f"{paid}/{paid + shortfall}") is None


@FUZZ
@given(NONNEGATIVE, NONNEGATIVE, st.integers(min_value=1, max_value=4))
def test_unrepresentable_change_is_rejected(price, coins, remainder):
    paid = price + 5 * coins + remainder
    assert change_due(f"{paid}/{price}") is None


@pytest.mark.parametrize(
    "parser,raw",
    [
        (parse_coins, ""), (parse_coins, "5,,10"), (parse_coins, "5,"),
        (parse_coins, "ten"), (parse_coins, "-5,10"), (parse_coins, "0"),
        (parse_coins, None), (parse_coins, "５,10"),
        (slot_position, ""), (slot_position, "A"), (slot_position, "A0"),
        (slot_position, "A-1"), (slot_position, "1A"), (slot_position, "ß7"),
        (slot_position, "A７"), (slot_position, None),
        (change_due, ""), (change_due, "200"), (change_due, "200/150/5"),
        (change_due, "200/"), (change_due, "text/150"),
        (change_due, "-5/0"), (change_due, "0/-5"), (change_due, None),
    ],
)
def test_rejects_invalid_input(parser, raw):
    assert parser(raw) is None


@pytest.mark.parametrize(
    "parser,raw,expected",
    [
        (parse_coins, "5,10,25", [5, 10, 25]),
        (slot_position, "A1", (0, 0)),
        (slot_position, "z26", (25, 25)),
        (change_due, "0/0", "0 five-coins"),
        (change_due, "200/150", "10 five-coins"),
    ],
)
def test_valid_examples(parser, raw, expected):
    assert parser(raw) == expected
