# -*- coding: utf-8 -*-
"""Connection to SFTP via paramiko."""
from ftplib import FTP  # nosec
from typing import Optional
import logging
import os

from paramiko import SFTPClient
import paramiko

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
LOGGER = logging.getLogger(__name__)


class FTPClient:
    """Connection used to interact with FTP."""

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 21,
        timeout: int = 2 * 3600,
    ):
        """Initialize SFTP connection."""
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

        self._client: Optional[FTP] = None

    def __enter__(self):
        """Open context with FTP."""
        ftp = FTP()
        ftp.connect(host=self.hostname, port=self.port, timeout=self.timeout)
        ftp.login(user=self.username, passwd=self.password)
        self._client = ftp
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

        self._client.close()

    def check_connection_open(self):
        """Check connection is open."""
        if self._client is not None:
            return

        raise Exception(
            "Connection of SFTP is wrapped as context manager, "
            "please use `with` to open a connection."
        )

    def exists_file(self, ftp_path: str) -> bool:
        """Check if a file exists in FTP.

        Args:
            ftp_path: path to the file to download in FTP
        Returns:
            True when such file exists
        """
        self.check_connection_open()

        try:
            file_name = os.path.basename(ftp_path)
            remote_dir = os.path.dirname(ftp_path)
            # prepend a seperator if missing from the remote_dir
            if remote_dir == "" or remote_dir[0] != os.sep:
                remote_dir = os.sep + remote_dir

            if self._client.pwd() != remote_dir:
                self._client.cwd(remote_dir)

            file_list = self._client.nlst(remote_dir)

            for a_file in file_list:
                if file_name in a_file:
                    continue
                return False

        except IOError:
            return False

        return True

    def download_file(self, ftp_path: str, dir_local: str) -> bool:
        """Download a file specified from FTP.

        Args:
            ftp_path: path to the file to download in FTP
            dir_local: local directory to keep the downloaded file
        Returns:
            True when such file is downloaded
        """
        self.check_connection_open()

        if self._client.pwd() != ftp_path:
            self._client.cwd(ftp_path)

        file_list = self._client.nlst()

        for file_name in file_list:
            if file_name != ftp_path:
                continue

            LOGGER.info("Downloading file: %s", file_name)
            local_path = os.path.join(dir_local, file_name)
            with open(local_path, "wb") as file_handle:
                self._client.retrbinary(f"RETR {file_name}", file_handle.write)

            return True

        return False


class SecureFTPClient(FTPClient):
    """Connection used to interact with Secure FTP."""

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 2 * 3600,
    ):
        """Initialize SFTP connection."""
        super().__init__(
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            timeout=timeout,
        )

        self._client: Optional[SFTPClient] = None  # type: ignore

    def __enter__(self):
        """Open context."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
        )

        self._client = ssh.open_sftp()

        return self

    def exists_file(self, ftp_path: str) -> bool:
        """Check if a file existed in SFTP.

        Args:
            ftp_path: path to the file to download in SFTP
        Returns:
            True when such file exists
        """
        try:
            self._client.stat(ftp_path)
        except IOError:
            return False

        return True

    def download_file(self, ftp_path: str, dir_local: str) -> bool:
        """Download a file specified from SFTP.

        Args:
            ftp_path: path to the file to download in SFTP
            dir_local: local directory to keep the downloaded zip
        Returns:
            True when such file is downloaded
        """
        self.check_connection_open()

        # check if such file exists before request,
        # an empty file would be generated by the SFTP client otherwise
        if not self.exists_file(ftp_path):
            return False

        file_name = os.path.basename(ftp_path)
        local_path = os.path.join(dir_local, file_name)

        self._client.get(remotepath=ftp_path, localpath=local_path)

        return True
