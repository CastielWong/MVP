#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Auxiliary component."""
from typing import List

from requests import Response, Session
import numpy as np
import pandas as pd
import yaml


def get_url(url: str) -> Response:
    """Get the response from the URL.

    Args:
        url: URL to send the get request

    Returns:
        The response returned from URL
    """
    session = Session()

    with session as sess:
        response = sess.get(url)

    return response


def get_content_in_range(file_name: str, start: int, end: int) -> List[str]:
    """Retrieve file content at the range specified.

    Args:
        file_name: file to retrieve contents
        start: start line number
        end: end line number

    Returns:
        List of lines
    """
    results = []

    counter = 0

    with open(file_name, "r") as f_r:
        line = " "

        while line:
            counter += 1
            line = f_r.readline()

            if counter < start:
                continue

            results.append(line)

            if counter >= end:
                break

    return results


def format_float_with_precision(real: float) -> str:
    """Convert float to string with precision.

    By default, the output of a real number would be truncated to 6 decimal places,
    as well as keeping ".0" if it's supposed to be an integer, or appending trailing
    0(s) if such float number has less than 6 decimal places.

    When the real number has more than 6 decimal places, it would be outputted in
    scientific notation instead.

    This function is to ensure scientific notation won't be applied and all digits
    will be parsed into and kept as string.

    When output to csv, the syntax will be something like:
    `df.to_csv(..., float_format=format_float_with_precision, ...)`

    Args:
        real: float number, either in or not in scientific notation

    Returns:
        Converted string with all digits kept, without decimal point nor tailing 0
    """
    return np.format_float_positional(real, trim="-")


def convert_csv_to_yaml(
    path_csv: str, separator: str = ",", path_yaml: str = None
) -> None:
    """Convert data in a csv file to YAML.

    Args:
        path_csv: data in csv file
        separator: separator used in csv file
        path_yaml: data file outputted to YAML
    """
    if path_yaml is None:
        path_yaml = path_csv.replace(".csv", ".yaml")

    df = pd.read_csv(path_csv, sep=separator)

    with open(path_yaml, "w") as f_w:
        yaml.dump(df.to_dict(orient="records"), f_w)

    with open(path_yaml, "r") as f_r:
        print(f_r.readlines())

    return
