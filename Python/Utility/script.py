#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess


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
