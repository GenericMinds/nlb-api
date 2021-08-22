import ujson
import uuid
import boto3
import os
import logging
import humps

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from layers.shared.common_utils.response_utility import ResponseUtility
from layers.shared.common_models.kit_models import Kit, KitPresignedResponse


def handler(event, context):
    body = ujson.loads(event['body'])
    body = humps.decamelize(body)
    kit = Kit(**body, file_name=body['title'].replace(" ", ""))
    response = get_presigned_url(kit)
    return ResponseUtility.create_response(response, 201)


def get_presigned_url(kit: Kit) -> KitPresignedResponse:
    request = {
        'Bucket': os.environ['ASSET_BUCKET'],
        'Key': f"kits/{kit.kit_type}/{kit.file_name}/{kit.file_name}.zip",
        'ContentType': "application/zip",
        'Metadata': {
            'title': kit.title,
            'description': kit.description,
        }
    }

    s3_client: BaseClient = boto3.client('s3')
    try:
        presigned_url = s3_client.generate_presigned_url(ClientMethod='put_object', Params=request)
    except ClientError as e:
        logging.error(e)
        raise e
    return KitPresignedResponse(file_name=kit.file_name, presigned_url=presigned_url)
