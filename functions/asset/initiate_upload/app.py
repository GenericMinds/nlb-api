import ujson
import uuid
import boto3
import os
import logging
import humps

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from layers.shared.common_utils.response_utility import ResponseUtility
from layers.shared.common_models.asset_models import AssetMetaData, AssetPresignedResponse


def handler(event, context):
    body = ujson.loads(event['body'])
    body = humps.decamelize(body)
    asset_data = AssetMetaData(**body, id=uuid.uuid4().hex)
    response = _get_presigned_url(asset_data)
    return ResponseUtility.create_response(response, 201)


def _get_presigned_url(file_data: AssetMetaData):
    request = {
        'Bucket': os.environ['ASSET_BUCKET'],
        'Key': f"{file_data.asset_type}/{file_data.id}/{file_data.file_name}",
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
    return AssetPresignedResponse(asset_id=file_data.id, presigned_url=presigned_url)
