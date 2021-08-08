import ujson
import uuid
import boto3
import os
import logging
import humps

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from layers.shared.nlb_common.response_service import create_response
from utils.models import FileMetaData, FilePresignedResponse, FileMetaDataSchema


def handler(event, context):
    body = ujson.loads(event['body'])
    body = humps.decamelize(body)

    schema = FileMetaDataSchema()

    # Check if dictionary is empty.
    is_valid = not bool(schema.validate(body))

    if is_valid:
        response = _get_presigned_url(FileMetaData(**body))
        return create_response(response, 201)
    else:
        return create_response(schema.validate(body), 400)


def _get_presigned_url(file_data: FileMetaData):
    asset_id = uuid.uuid4().hex
    request = {
        'Bucket': os.environ['ASSET_BUCKET'],
        'Key': f"{file_data.asset_type}/{asset_id}/{file_data.file_name}",
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
    return FilePresignedResponse(asset_id=asset_id, presigned_url=presigned_url)
