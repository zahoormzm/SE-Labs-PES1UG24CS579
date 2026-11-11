"""Validate coin lists, slot codes and payment pairs for Lab 7."""

from string import ascii_letters


MAX_DECIMAL_DIGITS = 64


def _decimal(token):
    """Convert a bounded unsigned ASCII decimal token or return None."""
    if not (
        1 <= len(token) <= MAX_DECIMAL_DIGITS
        and token.isascii()
        and token.isdecimal()
    ):
        return None
    return int(token)


def parse_coins(coins_csv):
    """Return a list of positive coin values, or None for invalid input."""
    if not isinstance(coins_csv, str):
        return None
    coins = []
    for token in coins_csv.split(","):
        coin = _decimal(token.strip())
        if coin is None or coin == 0:
            return None
        coins.append(coin)
    return coins


def slot_position(code):
    """Convert a letter and positive column to zero-based coordinates."""
    if not isinstance(code, str):
        return None
    code = code.strip()
    if len(code) < 2 or code[0] not in ascii_letters:
        return None
    column = _decimal(code[1:])
    if column is None or column == 0:
        return None
    return ord(code[0].upper()) - ord("A"), column - 1


def change_due(payment):
    """Return the exact number of five-unit coins, or None if invalid."""
    if not isinstance(payment, str):
        return None
    parts = payment.split("/")
    if len(parts) != 2:
        return None
    paid, price = (_decimal(part.strip()) for part in parts)
    if paid is None or price is None or paid < price:
        return None
    coins, remainder = divmod(paid - price, 5)
    if remainder:
        return None
    return f"{coins} five-coins"


def _show_result(prompt, parser, label, error):
    result = parser(input(prompt))
    print(error if result is None else f"{label}: {result}")


def main():
    """Prompt for each input and show a validation message on bad input."""
    try:
        print("==== Running parse_coins ====")
        _show_result(
            "Enter coin values as CSV (e.g. 5,10,25): ",
            parse_coins,
            "Coins",
            "Invalid coins. Enter comma-separated positive integers.",
        )
        print("\n==== Running slot_position ====")
        _show_result(
            "Enter a slot code (e.g. B7): ",
            slot_position,
            "Row and Column",
            "Invalid slot. Enter a letter A-Z followed by a positive column.",
        )
        print("\n==== Running change_due ====")
        _show_result(
            "Enter paid/price (e.g. 200/150): ",
            change_due,
            "Change Due",
            "Invalid payment. Use paid/price with exact five-unit change.",
        )
    except EOFError:
        print("\nNo more input.")


if __name__ == "__main__":
    main()
