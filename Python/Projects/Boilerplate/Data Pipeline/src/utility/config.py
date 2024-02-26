# -*- coding: utf-8 -*-
"""Module for all subcommands."""
from argparse import ArgumentParser
from string import Template
from typing import Any, Dict
import os

import yaml

STRING_TO_OBJECT = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": bool,
}


def parse_yaml(file_name: str) -> ArgumentParser:
    """Read a YAML file then convert its configuration into ArgumentParser.

    Args:
        file_name: name of the YAML file

    Returns:
        ArgumentParser which capture all parameters inside the YAML
    """
    with open(file_name, "r", encoding="utf-8") as f_r:
        configuration = yaml.safe_load(f_r)

    parser = ArgumentParser(
        prog=configuration["prog"], description=configuration["description"]
    )

    for argument in configuration["arguments"]:
        if "type" in argument["component"]:
            type_in_string = argument["component"]["type"]
            argument["component"]["type"] = STRING_TO_OBJECT[type_in_string]

        parser.add_argument(argument["option"], **argument["component"])

    return parser


def substitute_env_variable(string: str) -> str:
    """Fill in environment variable with actual value.

    Args:
        string: plain string with/without environment variable(s),
    when no such variable, it would keep the same and nothing to change

    Returns:
        String value which has environment variable(s) substituted
    """
    template = Template(string)
    new_value = template.safe_substitute(os.environ)
    return new_value


def load_configuration_yaml(config_file: str) -> Dict[str, Any]:
    """Load configuration from YAML file.

    Environment variables will be updated with actual values when there are.

    Args:
        config_file: path to the configuration YAML file

    Returns:
        Dictionary of key - value configuration
    """
    with open(config_file, "r", encoding="utf-8") as f_r:
        config = yaml.safe_load(f_r)

        # replace environment variable with actual value
        for key_, value in config.items():
            # skip non-string value
            if not isinstance(value, str):
                continue
            config[key_] = substitute_env_variable(value)

    return config
