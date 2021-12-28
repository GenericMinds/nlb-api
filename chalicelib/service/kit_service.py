from typing import List

from chalicelib.enums import KitType
from chalicelib.gateway.kit_gateway import KitGateway
from chalicelib.model.kit import Kit
from chalicelib.model.kit_post_urls import KitPostUrls


class KitService:
    "Handles operations for Kits"

    @classmethod
    def post_kit(cls, title: str, kit_type: KitType, description: str) -> KitPostUrls:
        "Posts a kit to dynamodb and returns presigned urls to upload image and zip of kit"
        kit = Kit.create(kit_type, title, description)

        KitGateway.persist_kit(kit)

        return kit.to_post_urls()

    @staticmethod
    def get_kits(kit_type: KitType) -> List[Kit]:
        """
        Gets kits from dynamodb

        Filterable by kit type
        """
        return KitGateway.get_kits(kit_type)
