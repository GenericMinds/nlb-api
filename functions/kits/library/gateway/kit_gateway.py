from typing import List, Optional

from functions.kits.library.model.dynamodb.kit_record_dbo import KitRecordDbo
from functions.kits.library.model.kit import Kit


class KitGateway:
    "Gateway for operations from DynamoDB (wraps PynamoDB ORM)"
    @staticmethod
    def get_kits(kit_type: Optional[str] = None) -> List[Kit]:
        "Retrieve all kits based on kit type"
        if kit_type:
            filter_condition = KitRecordDbo.kit_type == kit_type
        else:
            filter_condition = None

        raw_kits = KitRecordDbo.scan(filter_condition=filter_condition)
        records = [record for record in raw_kits]
        return Kit.from_raw_kit_record_dbos(records)

    @staticmethod
    def persist_kit(kit: Kit) -> None:
        "Persist changes into DynamoDB"
        raw_kit_dbo = kit.to_raw_kit_dbo()
        raw_kit_dbo.save()
