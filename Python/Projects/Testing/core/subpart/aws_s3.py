# -*- coding: utf-8 -*-
"""Demo for AWS S3."""
from io import StringIO
from typing import Dict, TypeVar

from pandas import DataFrame
import boto3

S3 = TypeVar("S3")


class Connection:
    """Class used for S3 connection."""

    def __init__(self, endpoint_url: str, access_key: str, secret_key: str):
        """Initialize the client.

        Args:
            endpoint_url: URL to S3
            access_key: the access key
            secret_key: the secret key
        """
        self.client: S3 = boto3.client(
            service_name="s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def upload_dataframe(
        self, df: DataFrame, bucket_name: str, object_key: str
    ) -> Dict[str, str]:
        """Upload a DataFrame to S3.

        Args:
            df: DataFrame to upload
            bucket_name: name of the bucket to upload
            object_key: name of the key to keep

        Returns:
            Result of the response, sample result can be check via
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
        """
        csv_buffer = StringIO()
        df.to_csv(path_or_buf=csv_buffer, index=False)

        response = self.client.put_object(
            Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue()
        )

        return response
