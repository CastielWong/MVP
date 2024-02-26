#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Test the running of Apple file download."""
# import os
# import shutil
from datetime import date

# import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from src.vendor.apple import main as apple

_DUMMY_CONTENT = (
    "FileDate   Activated   ISIN    ... EffectiveDate\n"
    "20230110   0   KRD020020016    ... 20230110\n"
    "...\n"
    "20230110   0   KRD020023028    ... 20230110"
)
_PARAMS = {
    "file_source_date": date(2023, 1, 10),
}


def test_download(mocker: MockerFixture, monkeypatch):
    """Verify the download."""
    monkeypatch.setenv("APPLE_FTP_PASSWORD", "dummy")

    source_file = "/server/storage/dummy_20230201.csv"
    dir_target = "/opt/volume/"

    # # prepare for SecureFTPClient mocking
    # check = mocker.MagicMock()

    # mocker.patch("paramiko.SSHClient", mocker.MagicMock())
    # mocker.patch(
    #     "connection.ftp.SecureFTPClient.__enter__", return_value=check
    # )
    # mocker.patch(
    #     "connection.ftp.SecureFTPClient.__exit__",
    #     return_value=mocker.MagicMock(),
    # )

    apple.download(source_file=source_file, dir_target=dir_target)

    # # verify the `SecureFTPClient.download_file()` is called with expected parameters
    # check.download_file.assert_called_with(ftp_path=source_file, dir_local=dir_target)

    return


def test_archive(fs: FakeFilesystem):
    """Test archive function when a file is archived."""
    return


def test_validate(fs: FakeFilesystem):
    """Test validate function when a file is valid."""
    file_name = "dummy_file"

    print(file_name)

    # # when there is no such file
    # assert apple.validate(file_name) is False

    # fs.create_file(file_path=file_name, contents=f"{_DUMMY_CONTENT}\nLINE COUNT:  10")
    # assert apple.validate(file_name) is True

    return


def test_run(fs: FakeFilesystem, mocker: MockerFixture, monkeypatch):
    """Verify the running works."""
    # def mock_download(**kwargs):  # pylint: disable=W0613 (unused-argument)
    #     shutil.copy(dummy_file_path, expected_file_path)
    #     return expected_file_path

    # # set dummy value to environment variables needed
    # for item in ("HOST", "USERNAME", "PASSWORD"):
    #     monkeypatch.setenv(f"APPLE_FTP_{item}", "dummy")
    # monkeypatch.setenv("APPLE_FTP_PORT", "6326")
    # monkeypatch.setenv("ARCHIVE_VOLUME", "/archiving")
    # monkeypatch.setenv("ARCHIVE_PREFIX", "prefix")

    # dummy_file_path = "/server/storage/dummy_20230201.csv"
    # file_name = os.path.basename(dummy_file_path)
    # expected_archiving_path = "/archiving/prefix/krx"
    # expected_file_path = f"{expected_archiving_path}/{file_name}"

    # fs.create_file(
    #     file_path="/app/etc/vendor/apple.yaml",
    #     contents=(
    #         "---\n"
    #         "APPLE_FTP_SERVER: dummy_apple_ftp\n"
    #         "APPLE_FTP_PORT: 22\n"
    #         "APPLE_FTP_USERNAME: demo\n"
    #     ),
    # )
    # fs.create_file(
    #     file_path=dummy_file_path, contents=f"{_DUMMY_CONTENT}\nLINE COUNT:   10"
    # )

    # mocker.patch("sys.exit", return_value=None)
    # mocker.patch("pyodbc.connect", return_value=mocker.MagicMock())
    # mocker.patch(
    #     "connection.ftp.SecureFTPClient.__enter__",
    #     return_value=mocker.MagicMock(),
    # )
    # mocker.patch(
    #     "connection.ftp.SecureFTPClient.__exit__",
    #     return_value=mocker.MagicMock(),
    # )

    # # there shouldn't be such directory before the download process
    # assert os.path.exists(expected_archiving_path) is False
    # apple.run(input_name="", input_date_str="20231010")
    # assert os.path.exists(expected_archiving_path) is True

    # # run again to check if download function is triggered to get the data file
    # mocker.patch(
    #     "downloader.apple.main.download",
    #     side_effect=mock_download,
    # )
    # mocker.patch("downloader.apple.main.validate", return_value=True)

    # apple.run(input_name="", input_date_str="20231010")
    # assert os.path.exists(expected_file_path) is True

    return
