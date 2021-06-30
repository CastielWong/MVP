#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict
import os
import subprocess


def get_size_meta(root_path: str = ".") -> Dict[str, int]:
    """Get the amount of files and the total size inside a directory.

    Args:
        root_path: the directory to get size meta

    Returns:
        The size meta of the directory
    """
    counter = 0
    total_size = 0

    for dir_path, dir_names, file_names in os.walk(root_path):
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

    subprocess.run(commands)

    # out, err = subprocess.Popen(
    #     commands.split(), stdout=subprocess.PIPE
    # ).communicate()

    return
