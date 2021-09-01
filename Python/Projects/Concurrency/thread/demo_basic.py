#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo the basic usage of threading."""
import time
import threading

from colorama.ansi import AnsiFore
import colorama


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
    threads = [
        threading.Thread(
            target=greeter, args=("Apple", 10, colorama.Fore.GREEN), daemon=True
        ),
        threading.Thread(
            target=greeter, args=("Berry", 5, colorama.Fore.BLUE), daemon=True
        ),
        threading.Thread(
            target=greeter, args=("Coconut", 2, colorama.Fore.WHITE), daemon=True
        ),
        threading.Thread(
            target=greeter, args=("Date", 11, colorama.Fore.RED), daemon=True
        ),
    ]

    for job in threads:
        job.start()

    print(f"{colorama.Fore.YELLOW}This is the main thread.")

    for job in threads:
        job.join(timeout=2)

    print(f"{colorama.Fore.YELLOW}Main thread continues.")
    print(f"{colorama.Fore.YELLOW}Done.")

    return


if __name__ == "__main__":
    main()
