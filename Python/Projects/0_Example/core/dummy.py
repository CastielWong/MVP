# -*- coding: utf-8 -*-
"""Dummy module."""


def inner_func(string: str, number: int) -> str:
    """Inner function."""
    return f"{string}: {number}"


def outer_func(prefix: str, string: str, number: int) -> str:
    """Outer function."""
    postfix = inner_func(string=string, number=number + 1)

    return f"{prefix}\t{postfix}"
