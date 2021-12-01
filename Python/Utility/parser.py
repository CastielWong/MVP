#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate the construction of a parser."""
from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
    """Create the parser."""
    parser = ArgumentParser(description="Sample argument parser")
    parser.add_argument("-v", "--version", action="version", version="v0.0.1")

    mandatory = parser.add_argument_group("mandatory")
    mandatory.add_argument("x", metavar="X", type=float, help="the base")
    mandatory.add_argument("y", metavar="Y", type=int, help="the exponent")

    parser.add_argument(
        "integers",
        metavar="N",
        type=int,
        nargs="+",
        help="an integer for the accumulator",
    )
    parser.add_argument(
        "--sum",
        dest="accumulate",
        action="store_const",
        const=sum,
        default=max,
        help="sum the integers (default: find the max)",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["value", "equation"],
        default="value",
        required=True,
        help="print either a final value or the equation (default: only the value)",
    )
    parser.add_argument(
        "-f", "--freq", action="count", default=0, help="count the frequency"
    )

    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )

    return parser


def main():
    """Execute as the entry point."""
    parser = create_parser()

    args = parser.parse_args()

    result = args.accumulate(args.integers)

    answer = args.x ** args.y
    print(f"The answer is {answer}")

    output = result

    if args.mode == "equation":
        output = ""
        for i in args.integers:
            output += f"{str(i)} + "

        output = f"{output[:-3]} = {result}"

    print(output)

    if args.freq > 0:
        print(f"The frequency is {args.freq}")
    if args.verbose:
        print("Verbosity is on")

    return


if __name__ == "__main__":
    main()
