#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample code for the appropriate way to apply lock."""
from threading import Thread, RLock
from typing import List, Tuple
from datetime import datetime
import random
import time

from colorama import Fore

TRANSFER_LOCK = RLock()


# pylint: disable=R0903 (too-few-public-methods)
class Account:
    """Account class."""

    __slot__ = ["balance", "lock"]

    def __init__(self, balance=0):
        """Initialize Account.

        Args:
            balance: account balance
        """
        self.balance = balance
        self.lock = RLock()


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

    if id(from_account) < id(to_account):
        lock1, lock2 = (from_account.lock, to_account.lock)
    else:
        lock1, lock2 = (to_account.lock, from_account.lock)

    with lock1:
        with lock2:
            from_account.balance -= amount
            time.sleep(0.000)
            to_account.balance += amount

    return


def validate_bank(accounts: List[Account], total: int, quiet=False) -> None:
    """Validate if the total balance is still consistent in the bank.

    Args:
        accounts: all existing accounts
        total: total balance expected
        quiet: whether to print if balance is consistent
    """
    for acct in accounts:
        acct.lock.acquire()
    current = sum(a.balance for a in accounts)
    for acct in accounts:
        acct.lock.release()

    if current != total:
        print(
            f"{Fore.RED}"
            f"ERROR: Inconsistent account balance: ${current:,} vs ${total:,}"
        )
        return

    if not quiet:
        print(f"{Fore.YELLOW}All good: Consistent account balance: ${total:,}")

    return


def get_two_accounts(accounts) -> Tuple[Account, Account]:
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
