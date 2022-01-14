from typing import List, Optional

from pynamodb.expressions.condition import Comparison
from pynamodb.pagination import ResultIterator

from chalicelib.enums import KitType
from chalicelib.model.dynamodb.kit_dbo import KitDbo
from chalicelib.model.kit import Kit


class KitGateway:
    "Gateway for operations from DynamoDB (wraps PynamoDB ORM)"

    @classmethod
    def get_kits(cls, kit_type: KitType, title: Optional[str]) -> List[Kit]:
        "Retrieve all kits based on query params kit type and title"
        condition: Comparison = None
        if title:
            condition &= KitDbo.title.contains(title)

        if kit_type != KitType.NONE:
            raw_kits_iterable = KitDbo.kit_type_index.query(hash_key=kit_type.value, filter_condition=condition)
        else:
            raw_kits_iterable = KitDbo.scan(filter_condition=condition)
        return cls._get_kits_from_raw_kit_iterable(raw_kits_iterable)

    @classmethod
    def get_recent_kits(cls) -> List[Kit]:
        "Retrieves the top 10 newest kits"
        raw_kits_iterable = KitDbo.scan()
        kits = cls._get_kits_from_raw_kit_iterable(raw_kits_iterable)
        newest_to_oldest_kits = sorted(kits, reverse=True)
        most_recent_ten_kits = newest_to_oldest_kits[:10]
        return most_recent_ten_kits

    @staticmethod
    def persist_kit(kit: Kit) -> None:
        "Persist changes into DynamoDB"
        raw_kit_dbo = kit.to_raw_kit_dbo()
        raw_kit_dbo.save()

    @staticmethod
    def _get_kits_from_raw_kit_iterable(raw_kits_iterable: ResultIterator[KitDbo]) -> List[Kit]:
        "Takes a result iterable of KitDbos from a pynamodb scan/query and converts it to a list of kits"
        raw_kits = list(raw_kits_iterable)
        kits = [Kit.from_raw_kit_dbo(raw_kit) for raw_kit in raw_kits]
        return kits
