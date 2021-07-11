#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import modules to ensure they are callable
# which means can be called via `caller.xxx`
from . import entry
from .animal import Animal
from .fruit import Fruit

# define modules to import explicitly when `import *`
__all__ = ["entry", "Animal", "Fruit"]
