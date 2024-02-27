#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Test for metadata of Apple file."""
import pytest

from src.vendor.apple import metadata
from src.vendor.apple.metadata import FileMeta


@pytest.mark.parametrize(
    "file_name, expected",
    # fmt: off
    [
        # different prefix
        (
            "dummy_20230101.csv",
            FileMeta(prefix="dummy", date="20230101", extension="csv"),
        ),
        (
            "virtual_20230101.csv",
            FileMeta(prefix="virtual", date="20230101", extension="csv"),
        ),
        # different date
        (
            "dummy_20230201.csv",
            FileMeta(prefix="dummy", date="20230201", extension="csv"),
        ),
        (
            "dummy_20231231.csv",
            FileMeta(prefix="dummy", date="20231231", extension="csv"),
        ),
        # different extension
        ("dummy_20230101", FileMeta(prefix="dummy", date="20230101", extension=None)),
        (
            "dummy_20230101.csv",
            FileMeta(prefix="dummy", date="20230101", extension="csv"),
        ),
        (
            "dummy_20230101.txt",
            FileMeta(prefix="dummy", date="20230101", extension="txt"),
        ),
    ],
    # fmt: on
)
def test_retrieve_file_meta(file_name: str, expected: FileMeta):
    """Verify basic functionality of FileMeta retrieval."""
    actual = metadata.retrieve_file_meta(name=file_name)

    assert actual == expected
    return


@pytest.mark.parametrize(
    "file_name",
    [
        "abc",
        # incorrect date format
        "dummy_2023105.csv",
        "dummy_202310050.csv",
        "dummy_120231005.csv",
        # nonexistent extension
        "dummy_120231005.dat",
        # other
        "dummy20230101.csv",
        "dummy_20230101csv",
    ],
)
def test_retrieve_file_meta__not_matched(file_name: str):
    """Verify when a file name is not matched."""
    with pytest.raises(AttributeError) as exp:
        metadata.retrieve_file_meta(name=file_name)

        assert exp.value == "'NoneType' object has no attribute 'group'"
    return
