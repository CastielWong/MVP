#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample Python file for demonstration."""
# pylint: skip-file


class Demo:
    """Demo class."""

    def __init__(self, msg: str):
        """Initialize the instance."""
        self.msg = msg

    def printing(self):
        """Print to demo."""
        return f"Demo {self.msg}"
