#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Example Logging module."""
# pylint: disable=C0103(invalid-name)
from logging import NullHandler
import logging

# do not emit any log messages by default
logging.getLogger(__name__).addHandler(  # pylint: disable=E1101(no-member)
    NullHandler()
)
