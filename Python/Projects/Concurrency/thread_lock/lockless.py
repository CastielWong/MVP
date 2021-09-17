#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample code for non-lock version."""
from threading import Thread
from typing import List, Tuple
from datetime import datetime
import random
import time

from colorama import Fore


# pylint: disable=R0903 (too-few-public-methods)
class Account:
    """Account class."""

    __slots__ = ["balance"]

    def __init__(self, balance=0):
        """Initialize Account.

        Args:
            balance: account balance
        """
        self.balance = balance


def do_bank_stuff(accounts: List[Account], total: int) -> None:
    """Perform bank transaction.

    Args:
        accounts: list of two accounts
        total: the total balance for all existing accounts
    """
    for _ in range(1, 10_000):
        a1, a2 = get_two_accounts(accounts)
        amount = random.randint(1, 100)  # nosec
        do_transfer(a1, a2, amount)
        validate_bank(accounts, total, quiet=True)

    return


def do_transfer(from_account: Account, to_account: Account, amount: int) -> None:
    """Transfer money between accounts.

    Args:
        from_account: whose balance is to decrease
        to_account: whose balance is to increase
        amount: amount to transfer
    """
    if from_account.balance < amount:
        return

    from_account.balance -= amount
    time.sleep(0.000)
    to_account.balance += amount

    return


def validate_bank(accounts: List[Account], total: int, quiet: bool = False) -> None:
    """Validate if the total balance is still consistent in the bank.

    Args:
        accounts: all existing accounts
        total: total balance expected
        quiet: whether to print if balance is consistent
    """
    current = sum(a.balance for a in accounts)

    if current != total:
        print(
            f"{Fore.RED}"
            f"ERROR: Inconsistent account balance: ${current:,} vs ${total:,}",
            flush=True,
        )
        return

    if not quiet:
        print(
            f"{Fore.YELLOW}All good: Consistent account balance: ${total:,}",
            flush=True,
        )

    return


def get_two_accounts(accounts: List[Account]) -> Tuple[Account, Account]:
    """Pick up two accounts from the list randomly.

    Args:
        accounts: list of accounts to pick up

    Returns:
        Two accounts picked
    """
    a1 = random.choice(accounts)  # nosec

    a2 = a1
    while a2 == a1:
        a2 = random.choice(accounts)  # nosec

    return a1, a2


def main():
    """Execute the main workflow."""
    accounts = [
        Account(balance=5_000),
        Account(balance=10_000),
        Account(balance=7_500),
        Account(balance=7_000),
        Account(balance=6_000),
        Account(balance=9_000),
    ]

    total = 0
    for acct in accounts:
        total += acct.balance

    validate_bank(accounts, total)

    print(f"{Fore.RESET}Starting transfers...")

    tasks = [
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
    ]

    t0 = datetime.now()

    for thread in tasks:
        thread.start()
        thread.join(0.001)

    elapsed = datetime.now() - t0

    print(f"{Fore.RESET}Transfers complete ({elapsed.total_seconds():,.2f}) seconds.")

    validate_bank(accounts, total)


if __name__ == "__main__":
    main()
