# Lab 7: Fuzz Testing

**SRN:** PES1UG24CS579

**Application:** Vending Machine

**Original version:** [Assigned Lab 7 starter](https://github.com/SETAPESU26/L6_L7_30_vending_machine/tree/1d144e1/lab7)

**Implementation and commits:** [Vending Machine fork](https://github.com/zahoormzm/L6_L7_30_vending_machine/tree/main/lab7)

## Run

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python vending_machine.py
python -m pytest -q --hypothesis-show-statistics test_vending_machine.py
```

## Findings and input rules

| Function | Original failure | Fixed behaviour |
| --- | --- | --- |
| `parse_coins` | `None` raises `AttributeError`; `5,,10` raises `ValueError`. | Accepts comma-separated positive integers, with optional spaces around each value. Rejects empty tokens. |
| `slot_position` | `None` raises `TypeError`; an empty code raises `IndexError`. | Accepts one ASCII letter followed by a positive column. For example, `B7` maps to `(1, 6)`. |
| `change_due` | `None` raises `AttributeError`; `152/150` silently discards a remainder. | Accepts nonnegative `paid/price` pairs only when payment covers the price and change is exactly divisible by five. |

Invalid input returns `None`. The application displays a validation message
and continues to the next prompt. Numeric tokens are limited to 64 ASCII digits.

## Verification

The three unrestricted-input properties failed against the original program;
Hypothesis reduced each failure to `None`. The fixed program passes **37 tests**:
eight properties with 150 passing generated examples each, plus 29 explicit
cases. The properties check malformed inputs, valid input round trips, slot
coordinates, exact change, underpayment and unrepresentable remainders.

On the same input sequence (`5,,10`, `B7`, `200/150`), the original CLI stops
at the coin prompt. The fixed CLI rejects the coin list, then prints `(1, 6)`
and `10 five-coins`.
