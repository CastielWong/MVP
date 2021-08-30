#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
from logging import Logger
import os
import logging.config

import yaml

# retrieve current working directory
CWD = os.path.dirname(__file__)
PATH_LOG = os.path.join(CWD, "logs")
PATH_CONFIG = os.path.join(CWD, "custom.yaml")

if not os.path.exists(PATH_LOG):
    os.mkdir(PATH_LOG)

# set up the customized configuration
with open(PATH_CONFIG, "r") as fr:
    config = yaml.load(fr, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)

    return logger
