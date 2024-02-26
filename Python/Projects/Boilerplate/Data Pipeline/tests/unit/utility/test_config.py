#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Verify the config module is working properly."""
from typing import Any, Dict
import argparse
import os

from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from tests import DIR_RESOURCE
from utility import config
import pytest

CONTENTS = (
    "description: This is for testing\n"
    "prog: testing\n"
    "arguments:\n"
    "- option: --kind\n"
    "  component:\n"
    "    help: 'dummy help'\n"
    "    required: True\n"
)
DUMMY_FILE = "dummy.yaml"

DUMMY_ENV = {
    "JOB_ID": 111_111,
    "foo": "alpha",
    "bar": "beta",
}


def test_parse_yaml():
    """Verify the happy path for parse_yaml."""
    parser = config.parse_yaml(os.path.join(DIR_RESOURCE, "cli_all.yaml"))

    assert parser.prog == "demo"

    actual_options = parser.__dict__["_option_string_actions"].keys()
    for expected in ["name", "env", "flag"]:
        assert f"--{expected}" in actual_options

    return


@pytest.mark.parametrize(
    "type_, expected",
    [
        ("boolean", bool),
        ("integer", int),
        ("float", float),
        ("string", str),
    ],
)
def test_parse_yaml__type(fs: FakeFilesystem, type_: str, expected: Any):
    """Verify the argument type is parsed correctly."""
    # pylint: disable=W0212 (protected-access)
    contents = CONTENTS + f"    type: {type_}\n"
    fs.create_file(file_path=DUMMY_FILE, contents=contents)

    parser = config.parse_yaml(DUMMY_FILE)

    for action in parser._actions:
        if not isinstance(action, argparse._StoreAction):
            continue

        assert action.dest == "kind"
        assert action.type == expected

    return


@pytest.mark.parametrize(
    "raw, expected",
    [
        # normal cases
        ("/$foo", "/alpha"),
        ("/opt/$foo", "/opt/alpha"),
        ("/opt/$foo/$bar", "/opt/alpha/beta"),
        ("/opt/$foo/tmp/$bar", "/opt/alpha/tmp/beta"),
        # environment variable wrapped by bracket
        ("/${foo}", "/alpha"),
        ("/${bar}", "/beta"),
        # no env variable to substitute
        ("/opt/foo", "/opt/foo"),
        # no such environment variable
        ("/opt/$baz", "/opt/$baz"),
        # actual case
        ("/barra-model-ftp/jobs/$JOB_ID", "/barra-model-ftp/jobs/111111"),
    ],
)
def test_substitute_env_variable(mocker: MockerFixture, raw, expected):
    """Verify function to substitute environment variables."""
    mocker.patch.object(target=os, attribute="environ", new=DUMMY_ENV)

    actual = config.substitute_env_variable(raw)
    assert actual == expected

    return


@pytest.mark.parametrize(
    "raw, expected",
    [
        (
            "connection_string: DRIVER={FreeTDS}; SERVER=localhost,1433;",
            {"connection_string": "DRIVER={FreeTDS}; SERVER=localhost,1433;"},
        ),
        (
            "connection_string: DRIVER={FreeTDS}; SERVER=${foo},${JOB_ID};",
            {"connection_string": "DRIVER={FreeTDS}; SERVER=alpha,111111;"},
        ),
        (
            "---\ndata_volume: vol\nworking_dir: working\nqdb_load: load\n",
            {
                "data_volume": "vol",
                "working_dir": "working",
                "qdb_load": "load",
            },
        ),
        (
            "---\ndata_volume: ${foo}\nworking_dir: ${bar}\nqdb_load: ${bar}\n",
            {
                "data_volume": "alpha",
                "working_dir": "beta",
                "qdb_load": "beta",
            },
        ),
    ],
)
def test_load_configuration_yaml(
    mocker: MockerFixture, fs: FakeFilesystem, raw: str, expected: Dict[str, Any]
):
    """Verify the functionality of YAML configuration loading."""
    mocker.patch.object(target=os, attribute="environ", new=DUMMY_ENV)

    file_name = "dummy.yaml"
    fs.create_file(file_path=file_name, contents=raw)

    actual = config.load_configuration_yaml(file_name)
    assert actual == expected

    return
