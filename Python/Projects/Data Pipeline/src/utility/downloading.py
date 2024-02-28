# -*- coding: utf-8 -*-
"""Demo download."""
from mimetypes import guess_extension
from pathlib import Path
import logging
import os

from requests import Response

from src.connection.ftp import SecureFTPClient

LOGGER = logging.getLogger(__name__)


_SFTP_CONFIG = {
    "host": "dummy_host",
    "port": 22,
    "username": "dummy",
    "password": os.environ.get("DUMMY_FTP_PASSWORD", "notProvided"),
    "key_file": os.environ.get("DUMMY_FTP_KEYFILE", None),
}

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding
CONTENT_ENCODING_TO_EXTENSION = {
    "gzip": ".gz",
    "compress": ".lzw",
    "deflate": ".zz",
    "br": ".br",
}

COMPRESSION_EXTENSIONS = [".gz", ".7z", ".zip"]


def download_from_ftp(source_file: str, dir_target: str) -> None:
    """Download a data file from SFTP.

    Args:
        source_file: path of the data file to download in the source
        dir_target: directory of the file downloaded in archiving volume
    """
    with SecureFTPClient(**_SFTP_CONFIG) as client:
        client.download_file(ftp_path=source_file, dir_local=dir_target)

    LOGGER.info(f"The source file {source_file} is downloaded in {dir_target}.")

    return


def download_raw_response(  # noqa: C901 (complex-structure)
    response: Response,
    file_path: str,
    chunk_size: int = 4096,
    is_stream: bool = True,
    overwrite: bool = False,
) -> str:
    """Download a response to file without decompressing.

    If header indicates the response is compressed, the relevant extensions are appended
    to the file path.

    Args:
        response: A response object
        file_path: Destination filepath
        chunk_size: Number of bytes to read into memory
        is_stream: Whether the request had stream enabled. Reduces memory usage,
            and in general should be turned on but can be turned off for small requests
        overwrite: Whether we overwrite if a file already exists at the destination
            path.
            This takes into account potential compression extensions before checking.

    Returns:
        The file path the was written to
    """
    # pytest.param("application/gzip", "", "dir/file.csv", "dir/file.csv.gz", False),

    content_type = response.headers.get("Content-Type", "")

    # content encoding can be layered, i.e: "deflate, gzip"
    content_encodings = response.headers.get("Content-Encoding", "")
    content_encodings = [  # type: ignore
        e.strip() for e in content_encodings.split(",") if e
    ]

    file_name = Path(file_path).name
    path_ext = file_name[file_name.index(".") :] if "." in file_name else ""
    # System-wide file associations are generally stored in /etc/mime.types
    # and the completeness of this file can vary from system to system
    if content_type == "application/gzip":
        header_ext = ".gz"
    else:
        header_ext = str(guess_extension(content_type) or "")

    if header_ext in COMPRESSION_EXTENSIONS:
        if header_ext not in path_ext:
            file_path = file_path + header_ext
    elif header_ext and path_ext != header_ext and not content_encodings:
        LOGGER.warning(
            f"Provided path {file_path} doesn't match header derived "
            "extensions: {header_ext}"
        )

    encoding_ext = "".join(
        [CONTENT_ENCODING_TO_EXTENSION[e] for e in content_encodings]
    )
    if encoding_ext and not path_ext.endswith(encoding_ext):
        file_path = file_path + encoding_ext

    if os.path.exists(file_path) and not overwrite:
        raise FileExistsError(
            f"{file_path} already exists, and overwrite is set to {overwrite}"
        )
    LOGGER.info(f"Downloading response to: {file_path}")
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "wb") as fp:
        if is_stream:
            # if there is any content encoding, skip the decoding, download raw as-is
            # stream must be enabled on the request to be able to access raw
            for chunk in response.raw.stream(chunk_size, decode_content=False):
                fp.write(chunk)
        else:
            if content_encodings:
                raise ValueError(
                    f"response contains content encodings: {content_encodings} "
                    "but is_stream isn't turned on"
                )
            content = response.content
            fp.write(content)

    LOGGER.info("Response downloaded.")
    return file_path
