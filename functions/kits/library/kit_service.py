import boto3
import logging
import os

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from functions.kits.library.enums import ContentType, FileExtension
from functions.kits.library.models import Kit


class KitService:
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
            return s3_client.generate_presigned_url(ClientMethod='put_object', Params=request, ExpiresIn=1800)
        except ClientError as e:
            logging.error(e)
            raise e
