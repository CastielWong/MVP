# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for the main entry of Downloader."""
import os

from src import DIR_ETC
from src.apple import main as apple
from src.berry import main as berry
from src.utility import config

if __name__ == "__main__":
    parser = config.parse_yaml(os.path.join(DIR_ETC, "cli.yaml"))

    args = parser.parse_args()

    match args.vendor:
        case "apple":
            apple.run(input_name=args.input_name, input_date_str=args.input_date)
        case "berry":
            berry.run(input_name=args.input_name, input_date_str=args.input_date)
        case _:
            raise NotImplementedError("Not implemented yet")
