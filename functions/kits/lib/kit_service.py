import boto3
import logging
import os

from dataclasses import asdict
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from functions.kits.lib.enums import ContentType, FileExtension
from functions.kits.lib.models import Kit, KitPresignedResponse


class KitService:
    @staticmethod
    def put_kit_in_dynamodb(kit: Kit):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['KIT_TABLE'])
        return table.put_item(Item=asdict(kit))

    @staticmethod
    def generate_put_presigned_url(kit: Kit, content_type: ContentType):
        file_extension = FileExtension[content_type.name]
        request = {
            'Bucket': os.environ['ASSET_BUCKET'],
            'Key': f"kits/{kit.kit_type}/{kit.file_name}/{kit.file_name}.{file_extension.value}",
            'ContentType': content_type.value,
        }

        s3_client: BaseClient = boto3.client('s3')
        try:
            presigned_url = s3_client.generate_presigned_url(ClientMethod='put_object', Params=request, ExpiresIn=1800)
        except ClientError as e:
            logging.error(e)
            raise e
        return KitPresignedResponse(file_extension=file_extension.value, presigned_url=presigned_url)
