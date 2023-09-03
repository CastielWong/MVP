# -*- coding: utf-8 -*-
"""Connection module."""
from typing import List, Optional
import logging

from pyodbc import Cursor, Row
import pyodbc

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
LOGGER = logging.getLogger(__name__)


class SqlServer:
    """Connection to SQL Server database."""

    def __init__(self, server: str, port: int, username: str, password: str):
        """Initialize the connection."""
        self._conn_string = (
            "Driver={FreeTDS};"
            f"SERVER={server},{port};"
            f"UID={username};"
            f"PWD={password};"
        )
        self._connection = None

    def __enter__(self):
        """Open context."""
        self._connection = pyodbc.connect(
            self._conn_string,
            autocommit=True,
        )
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Close context."""
        # output exception message if something goes wrong
        for key_, val in [
            ("type", exc_type),
            ("value", exc_value),
            ("trace back", exc_tb),
        ]:
            msg = f"Exception {key_}: {val}"
            LOGGER.info(msg)

        self._connection.close()

    @property
    def cursor(self) -> Optional[Cursor]:
        """Acquire the cursor for connection."""
        if self._connection is None:
            return None
        return self._connection.cursor()

    def run_script(self, query: str) -> List[Row]:
        """Run a query.

        Args:
            query: a SQL query
        """
        if self.cursor is None:
            raise RuntimeError("The cursor of connection shouldn't be None")

        with self.cursor as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows
