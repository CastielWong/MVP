#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Tests for connection module."""

from pytest_mock import MockerFixture
from core.connection import SqlServer
import pytest

DUMMY_CONFIG = {
    "server": "localhost",
    "port": 1433,
    "username": "sa",
    "password": "dummy",
}
DUMMY_QUERY = "SELECT * FROM dummy"


def test_context_manager(mocker: MockerFixture):
    """Test context manager."""
    check_conn = mocker.MagicMock()
    mocker.patch("pyodbc.connect", return_value=check_conn)

    with SqlServer(**DUMMY_CONFIG) as conn:  # type: ignore
        assert isinstance(conn, SqlServer) is True

    check_conn.close.assert_called_once()
    return


def test_run_script__exception(mocker: MockerFixture):
    """Test run_script() when there is RuntimeError."""
    mocker.patch("pyodbc.connect", return_values=None)

    with pytest.raises(RuntimeError) as exc_info:
        sql_server = SqlServer(**DUMMY_CONFIG)
        sql_server.run_script(DUMMY_QUERY)

    # note the exception message can only be checked after but not in the context
    assert str(exc_info.value) == "The cursor of connection shouldn't be None"

    return


def test_run_script__called_with(mocker: MockerFixture):
    """Test run_script() to called with query specified."""
    expected = ["a", "b", "c"]

    mocker.patch("pyodbc.connect", return_values=mocker.MagicMock())

    with SqlServer(**DUMMY_CONFIG) as conn:  # type: ignore
        patcher_fetchall = mocker.patch.object(conn.cursor.__enter__(), "fetchall")
        patcher_fetchall.return_value = expected

        actual = conn.run_script(DUMMY_QUERY)

        # assert the query is called inside `execute()`
        conn.cursor.__enter__().execute.assert_called_with(DUMMY_QUERY)

        assert actual == expected

    return


def test_run_script__side_effect(mocker: MockerFixture):
    """Test run_script() for multiple time runs."""
    # simulate results returned by `cursor.execute()`
    results = [[("1st result",)], [("2nd",)], [("the third",)]]

    mocker.patch("pyodbc.connect", return_values=mocker.MagicMock())

    with SqlServer(**DUMMY_CONFIG) as conn:  # type: ignore
        # mock all results returned
        patcher_fetchall = mocker.patch.object(conn.cursor.__enter__(), "fetchall")
        patcher_fetchall.side_effect = results

        # assert the result for each run
        for expected in results:
            actual = conn.run_script(DUMMY_QUERY)
            assert actual == expected

    return
