# -*- coding: utf-8 -*-
"""Sample for simple ETL pipeline."""
from datetime import datetime
import logging
import os

from core.subpart.mssql_connection import MsSqlConnection

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
LOGGER = logging.getLogger(__name__)


def run() -> None:
    """Entrypoint to run the ETL."""
    LOGGER.info("Start the ETL.")
    start_dt = datetime.utcnow()

    # prepare_archiving(archived_path)
    # downloaded = get_downloading(file_name, archived_path)
    # extracted = perform_extract(downloaded)
    # transformed = perform_transform(extracted)
    # perform_load(transformed)

    end_dt = datetime.utcnow()

    with MsSqlConnection(os.environ["DB_CONN_STRING"]) as db_conn:
        db_conn.retrieve_pk_columns("db.schema.table")

    LOGGER.info("Run time: {%s}\t-\t{%s}", start_dt, end_dt)
    return
