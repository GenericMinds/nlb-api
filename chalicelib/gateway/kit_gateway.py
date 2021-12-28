from typing import List

from chalicelib.enums import KitType
from chalicelib.model.kit import Kit
from chalicelib.model.dynamodb.kit_dbo import KitDbo

class KitGateway:
    "Gateway for operations from DynamoDB (wraps PynamoDB ORM)"

    @staticmethod
    def get_kits(kit_type: KitType) -> List[Kit]:
        "Retrieve all kits based on kit type"
        filter_condition = KitDbo.kit_type == kit_type.value if kit_type != KitType.NONE else None

        raw_kits_iterable = KitDbo.scan(filter_condition=filter_condition)
        raw_kits = list(raw_kits_iterable)
        return Kit.from_raw_kit_dbos(raw_kits)

    @staticmethod
    def persist_kit(kit: Kit) -> None:
        "Persist changes into DynamoDB"
        raw_kit_dbo = kit.to_raw_kit_dbo()
        raw_kit_dbo.save()
