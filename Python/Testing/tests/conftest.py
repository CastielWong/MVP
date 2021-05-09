#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Dict

import pytest
import requests
import yaml
from pytest import MonkeyPatch

_CWD = os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch: MonkeyPatch):
    """Disable network call to avoid unexpected calling.
    Ref: https://realpython.com/pytest-python-testing/

    Args:
        monkeypatch: fixture helps to safely set/delete an attribute
    """

    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())
    return


@pytest.fixture(scope="package")
def mock_config_conn() -> Dict[str, Dict]:
    """Mock the configuration of connections from YAML file.

    Returns:
        Configuration for connection
    """
    path_conn = os.path.join(_CWD, "connection.yaml")

    with open(path_conn, "r") as fr:
        config = yaml.load(fr, Loader=yaml.FullLoader)

    yield config
