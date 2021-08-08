import json
import uuid
import boto3
import os
import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from layers.shared.nlb_common.response_service import create_response
from models.file_meta_data import FileMetaData


def handler(event, context):
    body = json.loads(event['body'])
    file_data = FileMetaData(**body)
    response = _get_presigned_url(file_data)
    return create_response(response, 201)


def _get_presigned_url(file_data: FileMetaData):
    asset_id = uuid.uuid4().hex
    request = {
        'Bucket': os.environ['ASSET_BUCKET'],
        'Key': f"{file_data.asset_type}/{asset_id}/{file_data.title}.zip",
        'Metadata': {
            'title': file_data.title,
            'description': file_data.description,
            'file_name': file_data.file_name,
            'asset_id': asset_id
        }
    }

    s3_client: BaseClient = boto3.client('s3')
    try:
        presigned_url = s3_client.generate_presigned_url(ClientMethod='put_object', Params=request)
    except ClientError as e:
        logging.error(e)
        return "Encountered an error while generating presigned url"
    return {
        'assetId': asset_id,
        'presignedUrl': presigned_url
    }
