import humps
import os

from dataclasses import dataclass, asdict, field
from typing import List

from functions.kits.library.enums import KitType
from functions.kits.library.model.dynamodb.kit_record_dbo import KitRecordDbo


@dataclass
class Kit:
    """
    Represents a Kit at a high level
    """
    file_name: str
    kit_type: KitType
    title: str
    description: str
    image_url: str = field(init=False)

    def __post_init__(self):
        image_url = f"https://{os.environ['ASSET_BUCKET']}.s3.amazonaws.com/kits/{self.kit_type}/{self.file_name}/{self.file_name}.jpg"
        self.image_url = image_url

    def to_raw_kit_dbo(self) -> KitRecordDbo:
        "Converts a Kit to a KitRecordDbo"
        raw_kit_dbo = KitRecordDbo()
        raw_kit_dbo.file_name = self.file_name
        raw_kit_dbo.kit_type = self.kit_type.value
        raw_kit_dbo.title = self.title
        raw_kit_dbo.description = self.description

        return raw_kit_dbo

    @classmethod
    def from_raw_kit_record_dbos(cls, raw_kits: List[KitRecordDbo]):
        "Converts a list of KitRecordDbos to a list of Kit instances"
        kits = [
            cls(
                file_name=raw_kit.file_name,
                kit_type=KitType(raw_kit.kit_type),
                title=raw_kit.title,
                description=raw_kit.description
            )
            for raw_kit in raw_kits
        ]

        return kits

    def camelize(self):
        return humps.camelize(asdict(self))
