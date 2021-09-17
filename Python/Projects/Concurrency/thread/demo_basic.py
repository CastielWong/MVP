#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo the basic usage of threading."""
from typing import NamedTuple
import time
import threading

from colorama import Fore
from colorama.ansi import AnsiFore

Fruit = NamedTuple("Fruit", [("name", str), ("amount", int), ("color", AnsiFore)])


def greeter(fruit: str, number: int, color: AnsiFore) -> None:
    """Print the amount of fruit.

    Args:
        fruit: fruit name
        number: the amount of iteration time
        color: printing color
    """
    for i in range(0, number):
        print(f"{color}Amount of {fruit}: \t{i}")
        time.sleep(1)
    return


def main() -> None:
    """Execute the main workflow."""
    fruits = [
        Fruit("Apple", 10, Fore.GREEN),
        Fruit("Berry", 5, Fore.BLUE),
        Fruit("Coconut", 2, Fore.WHITE),
        Fruit("Date", 11, Fore.RED),
    ]

    tasks = []
    for fruit in fruits:
        # thread would continue running if it's not a daemon thread
        thread = threading.Thread(
            target=greeter,
            args=(fruit.name, fruit.amount, fruit.color),
            daemon=True,
        )
        tasks.append(thread)

    for thread in tasks:
        thread.start()

    print(f"{Fore.YELLOW}This is the main thread.")

    for thread in tasks:
        thread.join(timeout=2)

    print(f"{Fore.YELLOW}Main thread continues.")
    print(f"{Fore.YELLOW}Done.")

    return


if __name__ == "__main__":
    main()
