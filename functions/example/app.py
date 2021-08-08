import json
import boto3
import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError


def handler(event, context):
    body = json.loads(event['body'])

    response = {
        'message': 'hello world',
        'upload': body['upload']
    }

    return {
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200,
        'body': json.dumps(response),
    }


def _upload_file(file_name: str, bucket: str, destination: str = None) -> str:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param destination: S3 destination name including sub-folder. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if destination is None:
        destination = file_name

    # Upload the file
    s3_client: BaseClient = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, destination)
    except ClientError as e:
        logging.error(e)
        return "Encountered an error will uploading asset"
    return "Successfully uploaded asset"
