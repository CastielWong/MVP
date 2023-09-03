# -*- coding: utf-8 -*-
"""Simulate a Microsoft SQL Server database connection."""
from typing import List, Set
import logging

from pyodbc import Cursor
import pyodbc

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
LOGGER = logging.getLogger(__name__)


QUERY_PK_COLUMNS = (
    "SELECT COLUMN_NAME\n"
    "FROM [{database}].[INFORMATION_SCHEMA].[TABLE_CONSTRAINTS] as tc\n"
    "   JOIN [{database}].[INFORMATION_SCHEMA].[CONSTRAINT_COLUMN_USAGE] as ccu\n"
    "       ON tc.CONSTRAINT_NAME = ccu.CONSTRAINT_NAME\n"
    "           AND tc.TABLE_NAME = ccu.TABLE_NAME\n"
    "WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'\n"
    "   AND ccu.TABLE_SCHEMA = '{schema}' AND ccu.TABLE_NAME = '{table}'"
)

QUERY_TABLE_EXISTED = (
    "SELECT 1\n"
    "FROM [{database}].[INFORMATION_SCHEMA].[TABLES]\n"
    "WHERE TABLE_SCHEMA = '{schema}'\n"
    "   AND  TABLE_NAME = '{table}'"
)


class MsSqlConnection:
    """Connection to a database."""

    def __init__(self, conn_string: str):
        """Initialize the class."""
        self._conn_string = conn_string
        self._connection = None

    def __enter__(self):
        """Open context."""
        self._connection = pyodbc.connect(self._conn_string, autocommit=True)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Close context."""
        for key_, val in [
            ("type", exc_type),
            ("value", exc_value),
            ("trace back", exc_tb),
        ]:
            msg = f"Exception {key_}: {val}"
            LOGGER.info(msg)

        self._connection.close()

    @property
    def cursor(self) -> Cursor:
        """Acquire the cursor for connection."""
        if self._connection is None:
            raise RuntimeError("The connection shouldn't be None")
        return self._connection.cursor()

    def retrieve_pk_columns(self, target_table: str) -> Set[str]:
        """Retrieve columns for primary key from the target table inside database.

        Args:
            target_table: target table for data file to load in, follow the format
        as <database>.<schema>.<table>

        Returns:
            A set of PK columns
        """
        columns = set()

        database, schema, table = target_table.split(".")

        query = QUERY_PK_COLUMNS.format(
            database=database,
            schema=schema,
            table=table,
        )

        with self.cursor as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                col_name, *_ = row
                columns.add(col_name)

        return columns

    def are_tables_available(self, db_tables: List[str]) -> bool:
        """Check if all tables are available.

        Args:
            db_tables: table in the format of <database>.<schema>.<table>

        Returns:
            True is all tables are available, False if not
        """
        for db_table in db_tables:
            database, schema, table = db_table.split(".")

            with self.cursor as cursor:
                query = QUERY_TABLE_EXISTED.format(
                    database=database, schema=schema, table=table
                )

                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                except RuntimeError as ex:
                    LOGGER.exception("There is no such table: %s", ex)
                    return False

                if len(rows) == 0:
                    return False

        return True
