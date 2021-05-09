#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import dirname
from typing import TypeVar

import boto3
import pytest

_CWD = dirname(__file__)
_PATH_PACKAGE = dirname(dirname(_CWD))

# dynamic class generated, which is a subclass of "boto3.resources.base.ServiceResource"
ResourceS3 = TypeVar("ResourceS3")


@pytest.fixture(scope="package")
def mock_s3_resource() -> ResourceS3:
    s3_resource = boto3.resource(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="mock-access-key",
        aws_secret_access_key="mock-secret-key",
    )
    yield s3_resource
