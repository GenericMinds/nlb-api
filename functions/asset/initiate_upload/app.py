import ujson
import uuid
import boto3
import os
import logging
import humps

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from layers.shared.common_utils.response_utility import create_response
from utils.models import FileMetaData, FilePresignedResponse


def handler(event, context):
    body = ujson.loads(event['body'])
    body = humps.decamelize(body)
    file_data = FileMetaData(**body)
    response = _get_presigned_url(file_data)
    return create_response(response, 201)


def _get_presigned_url(file_data: FileMetaData):
    asset_id = uuid.uuid4().hex
    request = {
        'Bucket': os.environ['ASSET_BUCKET'],
        'Key': f"{file_data.asset_type}/{asset_id}/{file_data.file_name}",
        'ContentType': file_data.content_type,
        'Metadata': {
            'title': file_data.title,
            'description': file_data.description,
        }
    }

    s3_client: BaseClient = boto3.client('s3')
    try:
        presigned_url = s3_client.generate_presigned_url(ClientMethod='put_object', Params=request)
    except ClientError as e:
        logging.error(e)
        return "Encountered an error while generating presigned url"
    return FilePresignedResponse(asset_id=asset_id, presigned_url=presigned_url)