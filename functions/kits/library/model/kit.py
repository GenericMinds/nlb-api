from __future__ import annotations
import os

from dataclasses import dataclass
from typing import List

from functions.kits.library.enums import KitType
from functions.kits.library.model.dynamodb.kit_dbo import KitDbo
from functions.kits.library.types import Json


@dataclass
class Kit:
    """
    Represents a Kit at a high level
    """
    file_name: str
    kit_type: KitType
    title: str
    description: str
    image_url: str

    @classmethod
    def create(cls, kit_type: KitType, title: str, description: str) -> Kit:
        "Creates a Kit"
        file_name = title.replace(" ", "")

        attributes = {
            "file_name": file_name,
            "kit_type": kit_type,
            "title": title,
            "description": description,
            "image_url": f"https://{os.environ['ASSET_BUCKET']}.s3.amazonaws.com/kits/{kit_type.value}/{file_name}/{file_name}.jpg" 
        }

        return cls(**attributes)

    def to_raw_kit_dbo(self) -> KitDbo:
        "Converts a Kit to a KitDbo"
        raw_kit_dbo = KitDbo()
        raw_kit_dbo.file_name = self.file_name
        raw_kit_dbo.kit_type = self.kit_type.value
        raw_kit_dbo.title = self.title
        raw_kit_dbo.description = self.description

        return raw_kit_dbo

    @classmethod
    def from_raw_kit_record_dbos(cls, raw_kits: List[KitDbo]) -> List[Kit]:
        "Converts a list of KitDbos to a list of Kit instances"
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

    def to_json(self) -> Json:
        "Transforms Kit into json"
        return {
            "fileName": self.file_name,
            "kitType": self.kit_type.value,
            "title": self.title,
            "description": self.description,
            "imageUrl": self.image_url
        }
