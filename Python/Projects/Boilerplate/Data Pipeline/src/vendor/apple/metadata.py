# -*- coding: utf-8 -*-
"""Metadata for Apple data."""
from dataclasses import dataclass
import os
import re

FILE_NAME_REGEX = re.compile(
    "^(?P<prefix>[a-z]*)"
    r"_(?P<date>\d{8})"
    "(.(?P<extension>(csv|txt)))?$"
)  # fmt: off


@dataclass
class FileMeta:
    """Data class for Apple data file."""

    date: str
    prefix: str
    extension: str


def retrieve_file_meta(name: str) -> FileMeta:
    """Retrieve file metadata from its file name.

    Args:
        name: name of the file, can either be a plain name or with path

    Returns:
        FileMeta of the file
    """
    file_name = os.path.basename(name)

    matcher = FILE_NAME_REGEX.match(file_name)

    meta = FileMeta(
        date=matcher.group("date"),
        prefix=matcher.group("prefix"),
        extension=matcher.group("extension"),
    )

    return meta
