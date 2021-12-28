import logging
from typing import Any, Mapping

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError


# pylint: disable=too-few-public-methods
class S3Gateway:
    "Gateway for operations from S3"

    @staticmethod
    def generate_presigned_url(request: Mapping[str, Any]) -> str:
        "Generates a presigned url for the given request"
        s3_client: BaseClient = boto3.client("s3")
        try:
            return s3_client.generate_presigned_url(ClientMethod="put_object", Params=request, ExpiresIn=1800)
        except ClientError as error:
            logging.error(error)
            raise error
