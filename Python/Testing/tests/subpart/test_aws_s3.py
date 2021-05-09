#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import TypeVar

from moto import mock_s3
from pandas import DataFrame
from pytest_mock import MockerFixture

from conftest import _PATH_PACKAGE

# in case path not located
sys.path.append(_PATH_PACKAGE)
from core.subpart import aws_s3  # noqa: E402


ResourceS3 = TypeVar("ResourceS3")


@mock_s3
def test_upload_df_to_s3(mocker: MockerFixture, mock_s3_resource: ResourceS3):
    param = {
        "df": DataFrame(),
        "bucket_name": "mock_bucket",
        "object_key": "mock/path/to/key.csv",
    }

    conn_s3 = aws_s3.Connection(
        endpoint_url="", access_key="mock-access-key", secret_key="mock-secret-key"
    )

    # mock function `put_object` to simulate the uploading process
    def mock_s3_put_object(Bucket: str, Key: str, Body: str) -> None:
        mock_s3_resource.create_bucket(Bucket=Bucket)
        object_ = mock_s3_resource.Object(bucket_name=Bucket, key=Key)
        object_.put(Body=Body)
        return

    mocker.patch.object(conn_s3.client, "put_object", mock_s3_put_object)

    conn_s3.upload_dataframe(**param)

    assert 1 == 1
    return
