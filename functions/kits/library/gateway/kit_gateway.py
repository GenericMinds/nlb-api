from typing import List

from functions.kits.library.model.dynamodb.kit_dbo import KitDbo
from functions.kits.library.model.kit import Kit, KitType


class KitGateway:
    "Gateway for operations from DynamoDB (wraps PynamoDB ORM)"
    @staticmethod
    def get_kits(kit_type: KitType) -> List[Kit]:
        "Retrieve all kits based on kit type"

        filter_condition = KitDbo.kit_type == kit_type if kit_type != KitType.NONE else None 

        raw_kits = KitDbo.scan(filter_condition=filter_condition)
        records = [record for record in raw_kits]
        return Kit.from_raw_kit_record_dbos(records)

    @staticmethod
    def persist_kit(kit: Kit) -> None:
        "Persist changes into DynamoDB"
        raw_kit_dbo = kit.to_raw_kit_dbo()
        raw_kit_dbo.save()
