#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
import unittest

from .context import sample


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True


if __name__ == "__main__":
    unittest.main()
