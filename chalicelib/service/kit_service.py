import os

from chalicelib.enums import ContentType, FileExtension, KitType
from chalicelib.gateway.kit_gateway import KitGateway
from chalicelib.gateway.s3_gateway import S3Gateway
from chalicelib.model.kit import Kit
from chalicelib.model.responses.get_kits_response import GetKitsResponse
from chalicelib.model.responses.post_kit_response import PostKitResponse


class KitService:
    "Handles operations for Kits"

    # pylint: disable=fixme
    # TODO: Persist S3Gateway creation for subsequent calls

    @classmethod
    def post_kit(cls, title: str, kit_type: KitType, description: str) -> PostKitResponse:
        "Posts a kit to dynamodb and returns presigned urls to upload image and zip of kit"
        kit = Kit.create(kit_type, title, description)

        KitGateway.persist_kit(kit)

        return PostKitResponse.create(
            file_name=kit.file_name,
            image_presigned_url=cls._generate_put_presigned_url(kit.file_name, kit.kit_type, ContentType.JPEG, True),
            zip_presigned_url=cls._generate_put_presigned_url(kit.file_name, kit.kit_type, ContentType.ZIP),
        )

    @staticmethod
    def get_kits(kit_type: KitType) -> GetKitsResponse:
        """
        Gets kits from dynamodb

        Filterable by kit type
        """

        kits = KitGateway.get_kits(kit_type)
        return GetKitsResponse.create(kits)

    @staticmethod
    def get_recent_kits() -> GetKitsResponse:
        "Gets the most recent 10 kits from dynamodb"

        kits = KitGateway.get_recent_kits()
        return GetKitsResponse.create(kits)

    @staticmethod
    def _generate_put_presigned_url(file_name: str, kit_type: KitType, content_type: ContentType, public: bool = False) -> str:
        "Generates a presigned url for the kit to upload assets to AssetBucket"
        file_extension = FileExtension[content_type.name]

        request = {
            "Bucket": os.environ["ASSET_BUCKET"],
            "Key": f"kits/{kit_type.value}/{file_name}/{file_name}.{file_extension.value}",
            "ContentType": content_type.value,
            "ACL": "public-read" if public else "private",
        }

        return S3Gateway.generate_presigned_url(request)
