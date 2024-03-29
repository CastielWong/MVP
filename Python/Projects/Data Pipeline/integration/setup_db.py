#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize environment needed for local database.

Assuming the database is SQL Server.
"""
from string import Template
import logging
import os
import time

import pyodbc
import yaml

DB_CONFIG = "database.yaml"
PIPELINES = ("apple",)
INIT_SQL_SCRIPTS = [
    ("generate_records.sql", 5),
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
LOGGER = logging.getLogger(__name__)


def run_sql_script(db_conn_string: str, path_script: str, sec_to_wait: int) -> None:
    """Run SQL from a script file.

    Note that there is an issue when running t-sql in this way.
    The script may break before it insert all records needed, as Python
    keeps running without the script finishes.
    Setting waiting seconds is a quick workaround.

    Args:
        db_conn_string: connection string for SQL Server
        path_script: path to the SQL script file
        sec_to_wait: seconds to wait for the query to finish record populating
    """
    LOGGER.info("Running SQL script: %s", path_script)
    with open(path_script, "r", encoding="utf-8") as f_r:
        queries = f_r.readlines()

    with pyodbc.connect(db_conn_string, autocommit=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute("".join(queries))
            cursor.commit()

        time.sleep(sec_to_wait)

    return


def main() -> None:
    """Set the main entry point."""
    with open(DB_CONFIG, "r", encoding="utf-8") as f_r:
        raw_conn = yaml.safe_load(f_r)["connection_string"]
    conn_string = Template(raw_conn).safe_substitute(os.environ)

    # initialize database first
    run_sql_script(
        db_conn_string=conn_string,
        path_script="initialization/database.sql",
        sec_to_wait=1,
    )
    run_sql_script(
        db_conn_string=conn_string,
        path_script="initialization/table.sql",
        sec_to_wait=1,
    )

    for pipeline in PIPELINES:
        LOGGER.info("Set up for '%s' pipeline", pipeline)
        for script, seconds in INIT_SQL_SCRIPTS:
            script_file = os.path.join(pipeline, script)
            run_sql_script(
                db_conn_string=conn_string, path_script=script_file, sec_to_wait=seconds
            )

    return


if __name__ == "__main__":
    main()
