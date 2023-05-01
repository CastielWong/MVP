# -*- coding: utf-8 -*-
"""The context setup for subpart tests."""
from os.path import dirname
from typing import Generator, TypeVar

import boto3
import pytest

_CWD = dirname(__file__)
_PATH_PACKAGE = dirname(dirname(_CWD))

# dynamic class generated, which is a subclass of "boto3.resources.base.ServiceResource"
ResourceS3 = TypeVar("ResourceS3")


@pytest.fixture(scope="package")
def mock_s3_resource() -> Generator[ResourceS3, None, None]:
    """Mock to provide the S3 resource object."""
    s3_resource = boto3.resource(  # nosec
        "s3",
        region_name="us-east-1",
        aws_access_key_id="mock-access-key",
        aws_secret_access_key="mock-secret-key",
    )
    yield s3_resource
