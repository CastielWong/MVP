#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Verify if an ID is valid."""
from typing import List

COEFFICIENT = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
MAPPER = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]


def verify(check: List[int], check_code: str) -> bool:
    """Verify the check code.

    There is a corresponding coefficient for each of the first 17 digits.
    Sum up the first 17 digits with their coefficients, then acquire the mod
    by dividing with 11.
    The 18th digit should be that after mapping the mod.

    Args:
        check: list of the first 17 digits
        check_code: the 18th digit

    Returns:
        True if the check code matched
    """
    if len(check) != 17:
        print("The number of digits is invalid.")
        return False
    accumulator = 0
    for digit, coef in zip(check, COEFFICIENT):
        accumulator += digit * coef

    mod = accumulator % 11

    return check_code == MAPPER[mod]


def main(id_: str) -> None:
    """Run as the main.

    Args:
        id_:
    """
    check = [int(digit) for digit in id_[:-1]]

    is_valid = verify(check=check, check_code=id_[-1])

    print(f"Result of verification: {is_valid}")

    return


if __name__ == "__main__":
    main(id_="123456200001011239")
