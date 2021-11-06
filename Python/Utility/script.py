#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides functions for common usages."""
from multiprocessing import Pool
from typing import Dict, List
import os
import subprocess  # nosec


def count_lines(directory: str, cpu_count: int = None) -> List[int]:
    """Apply multiprocessing to count total lines inside a directory.

    Args:
        directory: directory to count lines
        cpu_count: cpu core to utilize

    Returns:
        List of amount of lines for each file
    """

    def counting(path_file: str) -> int:
        """Count lines for a file.

        Args:
            path_file: file to count lines

        Returns:
            Amount of lines in the file
        """
        lines = sum(1 for _ in open(path_file))
        return lines

    if cpu_count is None:
        cpu_count = os.cpu_count()

    file_list = os.listdir(directory)
    with Pool(cpu_count) as pool:
        results = pool.map(counting, file_list)

    return results


def get_size_meta(root_path: str = ".") -> Dict[str, int]:
    """Get the amount of files and the total size inside a directory.

    Args:
        root_path: the directory to get size meta

    Returns:
        The size meta of the directory
    """
    counter = 0
    total_size = 0

    for dir_path, _, file_names in os.walk(root_path):
        for file_name in file_names:
            fp = os.path.join(dir_path, file_name)

            # skip if it's a symbolic link
            if os.path.islink(fp):
                continue

            counter += 1
            total_size += os.path.getsize(fp)

    meta = {
        "amount": counter,
        "size": total_size,
    }
    return meta


def access_link_in_chrome_incognito(url: str) -> None:
    """Open the URL link in incognito mode on Chrome.

    Args:
        url: URL to check
    """
    commands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--args",
        "--incognito",
        url,
    ]

    subprocess.run(commands, check=True)  # nosec

    # out, err = subprocess.Popen(
    #     commands.split(), stdout=subprocess.PIPE
    # ).communicate()

    return
