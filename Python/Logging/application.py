#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
import logging
import os

import utility

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(utility.PATH_LOG, "root.log"),
    filemode="w",
    format="%(asctime)s - %(name)s - (%(module)-10s, %(lineno)d): %(message)s",
)


def log_from_root(message: str):
    logging.debug(f"DEBUG - {message}")
    logging.info(f"INFO - {message}")
    logging.warning(f"WARNING - {message}")
    logging.error(f"ERROR - {message}")
    logging.critical(f"CRITICAL - {message}")

    return
