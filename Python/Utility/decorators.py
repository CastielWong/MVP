#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provide common decorators as utilities."""
from typing import Any
import functools
import time


def timer(func):
    """Print the runtime of the decorated function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()

        value = func(*args, **kwargs)

        end_time = time.perf_counter()
        time_elapsed = end_time - start_time
        print(f"Time elapsed {func.__name__!r} in {time_elapsed:,.4f} secs")

        return value

    return wrapper


def debug(func):
    """Print the function signature and return value.

    This decorator is especially useful in recursive functions.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling `{func.__name__}({signature})`")

        value = func(*args, **kwargs)

        print(f"Function {func.__name__!r} returned {value!r}")

        return value

    return wrapper
