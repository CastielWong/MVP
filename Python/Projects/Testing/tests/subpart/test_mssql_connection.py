#!/usr/bin/env -S pytest
# -*- coding: utf-8 -*-
"""Test the Microsoft SQL Server connection module."""
from pytest_mock import MockerFixture
from core.subpart.mssql_connection import MsSqlConnection, QUERY_PK_COLUMNS

DUMMY_CONN_STRING = "dummy"
DUMMY_TABLE = "dummy_db.schema.table"


def test_context_manager(mocker: MockerFixture):
    """Test context manager."""
    check_conn = mocker.MagicMock()
    mocker.patch("pyodbc.connect", return_value=check_conn)

    with MsSqlConnection(DUMMY_CONN_STRING) as client:
        assert isinstance(client, MsSqlConnection) is True

    check_conn.close.assert_called_once()

    return


def test_retrieve_pk_columns(mocker: MockerFixture):
    """Test basic functionality to retrieve PK columns."""
    mocker.patch("pyodbc.connect", return_value=mocker.MagicMock())

    expected = {"col_a", "col_b", "col_c"}
    with MsSqlConnection(DUMMY_CONN_STRING) as client:
        patcher = mocker.patch.object(client.cursor.__enter__(), "fetchall")
        results = []
        for res in expected:
            results.append((res,))
        patcher.return_value = results

        actual = client.retrieve_pk_columns(DUMMY_TABLE)

        client.cursor.__enter__().execute.assert_called_with(
            QUERY_PK_COLUMNS.format(
                database="dummy_db",
                schema="schema",
                table="table",
            )
        )

        assert actual == expected

    return
