#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Test the ETL pipeline."""
from pytest_mock import MockerFixture
from core import etl
from core.subpart.mssql_connection import MsSqlConnection


def test_run(mocker: MockerFixture, monkeypatch):
    """Verify the ETL run."""
    monkeypatch.setenv("DB_CONN_STRING", "dummy_connection_string")

    mocker.patch("pyodbc.connect", return_value=mocker.MagicMock())

    # demo the usage of `spec`
    mocker.patch.object(MsSqlConnection, "__exit__", return_value=None)
    check_db = mocker.patch.object(
        MsSqlConnection,
        "__enter__",
        return_value=mocker.MagicMock(spec=MsSqlConnection),
    ).return_value

    check_db.retrieve_pk_columns.assert_not_called()
    etl.run()
    check_db.retrieve_pk_columns.assert_called_once()

    return
