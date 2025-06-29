#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Tests for connection module."""
from typing import Dict

from pytest_mock import MockerFixture
import pytest

from src.connection.database import (
    Connector,
    MySqlConnector,
    SqlServerConnector,
)

DUMMY_CONFIG_SQL_SERVER = {
    "server": "localhost",
    "port": 1433,
    "username": "sa",
    "password": "dummy",
}
DUMMY_CONFIG_MYSQL = {
    "host": "127.0.0.1",
    "port": 2223,
    "user": "root",
    "password": "dummy",
}
DUMMY_QUERY = "SELECT * FROM dummy"


###############################################################################
#   Assert Templates For Tests
###############################################################################


def _assert_run_script__exception(connector: Connector):
    """Assert template for when there is RuntimeError."""
    with pytest.raises(RuntimeError) as exc_info:
        connector.run_script(DUMMY_QUERY)

    # note the exception message can only be checked after but not in the context
    assert str(exc_info.value) == "The cursor of connection shouldn't be None"

    return


def _assert_run_script__called_with(mocker: MockerFixture, connector: Connector):
    """Assert template for called with query specified."""
    expected = ["a", "b", "c"]

    with connector as conn:
        patcher_execute = mocker.patch.object(conn.cursor.__enter__(), "execute")
        patcher_fetchall = mocker.patch.object(conn.cursor.__enter__(), "fetchall")
        patcher_fetchall.return_value = expected

        actual = conn.run_script(DUMMY_QUERY)

        # assert the query is called inside `execute()`
        patcher_execute.assert_called_with(DUMMY_QUERY)

        assert actual == expected

    return


def _assert_run_script__side_effect(mocker: MockerFixture, connector: Connector):
    """Test run_script() for multiple time runs."""
    # simulate results returned by `cursor.execute()`
    results = [[("1st result",)], [("2nd",)], [("the third",)]]

    with connector as conn:
        # mock all results returned
        patcher_fetchall = mocker.patch.object(conn.cursor.__enter__(), "fetchall")
        patcher_fetchall.side_effect = results

        # assert the result for each run
        for expected in results:
            actual = conn.run_script(DUMMY_QUERY)
            assert actual == expected

    return


###############################################################################
#   Tests
###############################################################################


@pytest.mark.parametrize(
    "mod_to_patch, connector, config",
    [
        ("pyodbc.connect", SqlServerConnector, DUMMY_CONFIG_SQL_SERVER),
        ("mysql.connector.connect", MySqlConnector, DUMMY_CONFIG_MYSQL),
    ],
)
def test__context_manager(
    mocker: MockerFixture, mod_to_patch: str, connector: Connector, config: Dict
):
    """Test context manager."""
    check_conn = mocker.MagicMock()
    mocker.patch(mod_to_patch, return_value=check_conn)

    with connector(**config) as conn:  # type: ignore
        assert isinstance(conn, connector) is True

    check_conn.close.assert_called_once()
    return


@pytest.mark.parametrize(
    "mod_to_patch, connector, config",
    [
        ("pyodbc.connect", SqlServerConnector, DUMMY_CONFIG_SQL_SERVER),
        ("mysql.connector.connect", MySqlConnector, DUMMY_CONFIG_MYSQL),
    ],
)
def test_run_script__exception(
    mocker: MockerFixture, mod_to_patch: str, connector: Connector, config: Dict
):
    """Test run_script() when there is RuntimeError."""
    mocker.patch(mod_to_patch, return_values=None)

    connector_instance = connector(**config)  # type: ignore
    _assert_run_script__exception(connector_instance)

    return


@pytest.mark.parametrize(
    "mod_to_patch, connector, config",
    [
        ("pyodbc.connect", SqlServerConnector, DUMMY_CONFIG_SQL_SERVER),
        ("mysql.connector.connect", MySqlConnector, DUMMY_CONFIG_MYSQL),
    ],
)
def test_run_script__called_with(
    mocker: MockerFixture, mod_to_patch: str, connector: Connector, config: Dict
):
    """Test run_script() to called with query specified."""
    mocker.patch(mod_to_patch, return_values=mocker.MagicMock())

    connector_instance = connector(**config)  # type: ignore
    _assert_run_script__called_with(mocker, connector_instance)

    return


@pytest.mark.parametrize(
    "mod_to_patch, connector, config",
    [
        ("pyodbc.connect", SqlServerConnector, DUMMY_CONFIG_SQL_SERVER),
        ("mysql.connector.connect", MySqlConnector, DUMMY_CONFIG_MYSQL),
    ],
)
def test_run_script__side_effect(
    mocker: MockerFixture, mod_to_patch: str, connector: Connector, config: Dict
):
    """Test run_script() for multiple time runs."""
    mocker.patch(mod_to_patch, return_values=mocker.MagicMock())

    connector_instance = connector(**config)  # type: ignore
    _assert_run_script__side_effect(mocker, connector_instance)

    return
