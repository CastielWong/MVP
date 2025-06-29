# -*- coding: utf-8 -*-
"""Logic for Berry data ETL."""
import logging

LOGGER = logging.getLogger(__name__)

_VENDOR_NAME = "berry"


def extract(source_file: str = "", target_path: str = "") -> bool:
    """Perform file extraction.

    Args:
        source_file: path/name of the file to extract
        target_path: path where file(s) is(are) extracted

    Returns:
        True if file is extracted successfully
    """
    return True


def validate(data_file: str = "") -> bool:
    """Perform data validation.

    Args:
        data_file: path to the data file for validation

    Returns:
        True if data is integral
    """
    return True


def transform(data_file: str = "", target_path: str = "") -> bool:
    """Perform data transformation.

    Args:
        data_file: path to the data file for transformation
        target_path: path used to store data after transformed

    Returns:
        True if file is transformed successfully
    """
    return True


def check_constraint(data_file: str = "") -> bool:
    """Perform constraint check on the data file after transformed.

    Args:
        data_file: path to the data file for constraint checking

    Returns:
        True if data pass all constraints
    """
    return True


def load(source: str = "", destination: str = "") -> bool:
    """Perform data load.

    Args:
        source: path to the data file for loading
        destination: where the data is loaded into

    Returns:
        True if file is loaded successfully
    """
    return True


def run(input_name: str, input_date_str: str) -> None:
    """Run the main process.

    Args:
        input_name: name of the input to kick off downloading
        input_date_str: date of input
    """
    extract()

    validate()

    transform()

    check_constraint()

    load()

    return
