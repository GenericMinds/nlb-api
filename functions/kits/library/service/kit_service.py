from typing import List, Optional

import boto3
import logging
import os

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from functions.kits.library.enums import ContentType, FileExtension, KitType
from functions.kits.library.gateway.kit_gateway import KitGateway
from functions.kits.library.model.kit import Kit
from functions.kits.library.model.kit_post_urls import KitPostUrls


class KitService:
    @classmethod
    def post_kit(cls, title: str, kit_type: KitType, description: str) -> KitPostUrls:
        kit = Kit.create(kit_type, title, description)

        KitGateway.persist_kit(kit)

        kit_post_urls = KitPostUrls.create(
            file_name=kit.file_name,
            image_presigned_url=cls._generate_put_presigned_url(kit, ContentType.JPEG, True),
            zip_presigned_url=cls._generate_put_presigned_url(kit, ContentType.ZIP)
        )

        return kit_post_urls

    @staticmethod
    def get_kits(kit_type: KitType) -> List[Kit]:
        return KitGateway.get_kits(kit_type)

    @staticmethod
    def _generate_put_presigned_url(kit: Kit, content_type: ContentType, public: bool = False) -> str:
        file_extension = FileExtension[content_type.name]

        request = {
            "Bucket": os.environ["ASSET_BUCKET"],
            "Key": f"kits/{kit.kit_type.value}/{kit.file_name}/{kit.file_name}.{file_extension.value}",
            "ContentType": content_type.value,
            "ACL": "public-read" if public else "private"
        }

        s3_client: BaseClient = boto3.client("s3")
        try:
            return s3_client.generate_presigned_url(ClientMethod="put_object", Params=request, ExpiresIn=1800)
        except ClientError as error:
            logging.error(error)
            raise error
