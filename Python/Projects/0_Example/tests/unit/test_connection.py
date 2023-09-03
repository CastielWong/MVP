#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Tests for connection module."""

from pytest_mock import MockerFixture
from core.connection import SqlServer

DUMMY_CONFIG = {
    "server": "localhost",
    "port": 1433,
    "username": "sa",
    "password": "dummy",
}


def test_context_manager(mocker: MockerFixture):
    """Test context manager."""
    check_conn = mocker.MagicMock()
    mocker.patch("pyodbc.connect", return_value=check_conn)

    with SqlServer(**DUMMY_CONFIG) as conn:  # type: ignore
        assert isinstance(conn, SqlServer) is True

    check_conn.close.assert_called_once()
    return


def test_run_script(mocker: MockerFixture):
    """Test running query."""
    query = "SELECT * FROM dummy"
    expected = ["a", "b", "c"]

    mocker.patch("pyodbc.connect", return_values=mocker.MagicMock())

    with SqlServer(**DUMMY_CONFIG) as conn:  # type: ignore
        patcher_fetchall = mocker.patch.object(conn.cursor.__enter__(), "fetchall")
        patcher_fetchall.return_value = expected

        actual = conn.run_script(query)

        # assert the query is called inside `execute()`
        conn.cursor.__enter__().execute.assert_called_with(query)

        assert actual == expected

    return
