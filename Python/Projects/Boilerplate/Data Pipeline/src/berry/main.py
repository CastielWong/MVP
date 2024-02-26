# -*- coding: utf-8 -*-
"""Logic for Berry data downloading."""
import logging

LOGGER = logging.getLogger(__name__)

_VENDOR_NAME = "berry"


def download(source_file: str = "", dir_target: str = "") -> bool:
    """Perform data downloading.

    Args:
        source_file: name/path of the source file
        dir_target: name/path of the directory to keep or persist the file

    Returns:
        True if the downloading is successful.
    """
    return True


def archive() -> bool:
    """Perform file archiving.

    Returns:
        True if file is archived successfully
    """
    return True


def validate(file_name: str = "") -> bool:
    """Perform file validation.

    Args:
        file_name: name/path of the file to validate

    Returns:
        True if such file is integral
    """
    return True


def run(input_name: str, input_date_str: str) -> None:
    """Run the main process.

    Args:
        input_name: name of the input to kick off downloading
        input_date_str: date of input
    """
    download()

    archive()

    validate()
    return
