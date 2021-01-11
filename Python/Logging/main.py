#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
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


def main() -> None:
    app.log_from_root()
    log_from_general()


if __name__ == "__main__":
    main()
