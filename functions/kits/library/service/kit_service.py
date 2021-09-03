from typing import Optional

import boto3
import logging
import os

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from functions.kits.library.enums import ContentType, FileExtension, KitType
from functions.kits.library.gateway.kit_gateway import KitGateway
from functions.kits.library.model.kit import Kit
from functions.kits.library.model.kit_url import KitUrls


class KitService:
    @classmethod
    def post_kit(cls, title: str, kit_type: KitType, description: str):
        kit = Kit(
            file_name=title.replace(" ", ""),
            kit_type=kit_type,
            title=title,
            description=description
        )

        KitGateway.persist_kit(kit)

        kit_urls = KitUrls(
            file_name=kit.file_name,
            image_presigned_url=cls._generate_put_presigned_url(kit, ContentType.JPEG),
            zip_presigned_url=cls._generate_put_presigned_url(kit, ContentType.ZIP)
        )

        return kit_urls

    @staticmethod
    def get_kits(kit_type: Optional[str] = None):
        kits = KitGateway.get_kits(kit_type)
        return kits

    @staticmethod
    def _generate_put_presigned_url(kit: Kit, content_type: ContentType):
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
