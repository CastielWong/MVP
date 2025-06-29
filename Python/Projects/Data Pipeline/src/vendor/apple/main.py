# -*- coding: utf-8 -*-
"""Logic for Apple data file acceptance."""
import logging

LOGGER = logging.getLogger(__name__)

_VENDOR_NAME = "apple"


def download(source_file: str = "", dir_target: str = "") -> bool:
    """Perform data downloading.

    Args:
        source_file: name/path of the source file
        dir_target: name/path of the directory to keep or persist the file

    Returns:
        True if the downloading is successful.
    """
    # with SecureFTPClient(**_SFTP_CONFIG) as client:
    #     client.download_file(ftp_path=source_file, dir_local=dir_target)

    # LOGGER.info(f"The source file {source_file} is downloaded in {dir_target}.")

    return True


def check_integrity(file_path: str = "", expected_hash: str = "") -> bool:
    """Perform sanity check on the downloaded file.

    Args:
        file_path: path/name of the file to validate
        expected_hash: the hash value acquired for sanity check

    Returns:
        True if the file is intact
    """
    return True


def archive(file_path: str = "") -> bool:
    """Perform file archiving.

    Args:
        file_path: path/name of the file to validate

    Returns:
        True if file is archived successfully
    """
    return True


def run(input_name: str, input_date_str: str) -> None:
    """Run the main process.

    Args:
        input_name: name of the input to kick off downloading
        input_date_str: date of input
    """
    download()

    check_integrity()

    archive()

    return
