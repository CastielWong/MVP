#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
import logging
import os

import utility
import application as app


def log_from_general() -> None:
    # make sure the name matches the customization
    logger = utility.get_logger("LogDemo")

    message = "from LogDemo"
    logger.debug(f"DEBUG - {message}")
    logger.info(f"INFO - {message}")
    logger.warning(f"WARNING - {message}")
    logger.error(f"ERROR - {message}")
    logger.critical(f"CRITICAL - {message}")

    return


def redirect_root_log(keep_log: bool = True) -> None:
    logger = logging.root

    # find then remove current file handler(s)
    for handler in logger.handlers:
        if not isinstance(handler, logging.FileHandler):
            continue

        # keep configuration for the last file handler
        formatter = handler.formatter

        # remove the specified log if needed
        if not keep_log:
            os.remove(handler.baseFilename)
        # remove the file handler
        logger.removeHandler(handler)

        path_log = os.path.join(utility.PATH_LOG, "root_redirected.log")
        file_handler = logging.FileHandler(filename=path_log, mode="w")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return


def main() -> None:
    app.log_from_root("from application")
    log_from_general()

    redirect_root_log()
    app.log_from_root("after redirection")


if __name__ == "__main__":
    main()
