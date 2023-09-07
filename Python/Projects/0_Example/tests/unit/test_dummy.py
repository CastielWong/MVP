#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Module to test the dummy."""
from pytest_mock import MockerFixture
from core import dummy


def test_inner_func():
    """Test inner_func."""
    actual = dummy.inner_func(string="apple", number=2)

    assert actual == "apple: 2"
    return


def test_outer_func():
    """Test outer_func."""
    actual = dummy.outer_func(prefix="Fruit", string="apple", number=2)

    assert actual == "Fruit\tapple: 3"
    return


def test_outer_func__called_with(mocker: MockerFixture):
    """Test outer_func with expected parameter called."""
    patcher = mocker.patch("core.dummy.inner_func", return_value="nothing")

    actual = dummy.outer_func(prefix="Fruit", string="apple", number=2)

    patcher.assert_called_with(string="apple", number=3)
    assert actual == "Fruit\tnothing"
    return
