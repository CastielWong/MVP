#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation in multi-processing."""
from datetime import datetime
import math
import multiprocessing

from colorama import Fore
from colorama.ansi import AnsiFore

NUMBER = 30_000_000


def do_math(start: int = 0, stop: int = 10, color: AnsiFore = Fore.RESET) -> float:
    """Overload CPU computation by calculating number in power then square root.

    Args:
        start: start number
        stop: number until stop
        color: printing color

    Returns:
        Average over the calculated difference
    """
    summation = 0.0

    position = start
    # set a fair number to increase computation consumption
    k_sq = 1_000 * 1_000

    print(f"{color}This thread is taking care of range: [{start:,}, {stop:,})")

    while position < stop:
        if position % 2_000_000 == 0:
            print(f"{color}Computing reaches to position {position:>15,}...")

        position += 1
        diff = math.sqrt((position - k_sq) * (position - k_sq))

        summation += diff

    average = summation / (stop - start)
    print(
        f"{Fore.RESET}"
        f"Result when position {position:>10,} is reached: {average:>15,.3f}"
    )

    return average


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    processor_count = multiprocessing.cpu_count()
    print(f"There are {processor_count} processors in total.")

    processor_count = min(processor_count, 4)
    print(f"Doing math on {processor_count} processors.")

    color_mapping = {
        0: Fore.YELLOW,
        1: Fore.CYAN,
        2: Fore.GREEN,
        3: Fore.MAGENTA,
    }

    pool = multiprocessing.Pool()  # pylint: disable=R1732 (consider-using-with)
    tasks = []
    for index in range(processor_count):
        task = pool.apply_async(
            func=do_math,
            args=(
                int(NUMBER * index / processor_count),
                int(NUMBER * (index + 1) / processor_count),
                color_mapping[index],
            ),
        )
        tasks.append(task)

    pool.close()
    pool.join()

    print("The results: ")
    for i, task in enumerate(tasks):
        print(f"{i:>3} - {task.get():>15,.2f}")

    elapsed = datetime.now() - t0
    print(f"Done in {elapsed.total_seconds():,.2f} seconds.")

    return


if __name__ == "__main__":
    main()
