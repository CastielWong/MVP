#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Module to test the utility."""
import os

from pytest_mock import MockerFixture
from core import utility as util
import pytest

DUMMY_ENV = {
    "dummy": 111_111,
    "foo": "alpha",
    "bar": "beta",
}


@pytest.mark.parametrize(
    "raw, expected",
    [
        # normal cases
        ("/$foo", "/alpha"),
        ("/opt/$foo", "/opt/alpha"),
        ("/opt/$foo/$bar", "/opt/alpha/beta"),
        ("/opt/$foo/tmp/$bar", "/opt/alpha/tmp/beta"),
        # environment variable wrapped by bracket
        ("/${foo}", "/alpha"),
        ("/${dummy}", "/111111"),
        # no env variable to substitute
        ("/opt/foo", "/opt/foo"),
        # no such environment variable
        ("/opt/$baz", "/opt/$baz"),
    ],
)
def test_substitute_env_variable(mocker: MockerFixture, raw: str, expected: str):
    """Verify function to substitute environment variables."""
    mocker.patch.object(target=os, attribute="environ", new=DUMMY_ENV)

    actual = util.substitute_env_variable(raw)
    assert actual == expected

    return


@pytest.mark.parametrize(
    "real_number, expected",
    [
        # general cases
        (2, "2"),
        (1.2, "1.2"),
        (1.201, "1.201"),
        # decimal point
        (2.0, "2"),
        (1.20, "1.2"),
        (1.200_000, "1.2"),
        (1.200_000_00, "1.2"),
        (0.3, "0.3"),
        # scientific notation
        (1.0e3, "1000"),
        (1.0e16, "10000000000000000"),
        (1.001e16, "10010000000000000"),
        (1.0e-3, "0.001"),
        (8.123_456_789_123_45e-05, "0.0000812345678912345"),
        (8.123_456_789_123_45e-06, "0.00000812345678912345"),
        (8.123_456_789_123_45e-09, "0.00000000812345678912345"),
    ],
)
def test_format_float_with_precision(real_number: float, expected: str):
    """Test the float to string type formatting.

    Note that the code formatting tool like "black" would format input cases:
    - 2.0 -> 2.0
    - .3 -> 0.3
    - 1.0E3 -> 1.0e3
    - 1.0E+3 -> 1.0e3

    It's safe to assume that those corner cases would work without issue even
    not presented in the tests.
    """
    actual = util.format_float_with_precision(real_number)
    assert actual == expected

    return
