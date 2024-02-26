# -*- coding: utf-8 -*-
"""Initialization for unit tests.

`pyfakefs` is functioning as pytest plugin that provides the `fs` fixture,
which is registered at installation time
"""
import os

DIR_TEST = os.path.dirname(__file__)
DIR_RESOURCE = os.path.join(DIR_TEST, "resource")
