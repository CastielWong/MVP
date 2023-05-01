#!/usr/bin/env -S pytest
# -*- coding: utf-8 -*-
"""Test the AWS S3 module."""
from typing import TypeVar
import sys

# from boto3.resources.factory import s3
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
    """Verify file upload to S3."""
    param = {
        "df": DataFrame(),
        "bucket_name": "mock_bucket",
        "object_key": "mock/path/to/key.csv",
    }

    conn_s3 = aws_s3.Connection(
        endpoint_url="https://mock.com",
        access_key="mock-access-key",
        secret_key="mock-secret-key",
    )

    # mock function `put_object` to simulate the uploading process
    def mock_s3_put_object(Bucket: str, Key: str, Body: str):
        mock_s3_resource.create_bucket(Bucket=Bucket)
        object_ = mock_s3_resource.Object(bucket_name=Bucket, key=Key)
        object_.put(Body=Body)
        return object_

    mocker.patch.object(
        target=conn_s3.client, attribute="put_object", new=mock_s3_put_object
    )

    s3_object = conn_s3.upload_dataframe(**param)

    assert s3_object.bucket_name == param["bucket_name"]
    assert s3_object.key == param["object_key"]

    return
