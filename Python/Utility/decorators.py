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


def slow(_func=None, *, num_of_second: float = 1):
    """Slow down the function by 1 second before calling."""

    def inner_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            time.sleep(num_of_second)
            return func(*args, **kwargs)

        return wrapper

    if _func is None:
        return inner_decorator
    return inner_decorator(_func)


def singleton(cls):
    """Make a class a Singleton class (only one instance)."""

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if wrapper_singleton.instance is None:
            print("No existing instance, one is creating...")
            wrapper_singleton.instance = cls(*args, **kwargs)

        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton
