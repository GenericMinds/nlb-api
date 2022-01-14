from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime

from pytz import timezone

from chalicelib.enums import KitType
from chalicelib.model.dynamodb.kit_dbo import KitDbo
from chalicelib.types import Json


@dataclass
class Kit:
    "Represents a Kit at a high level"
    file_name: str
    kit_type: KitType
    title: str
    description: str
    image_url: str
    created_date: datetime

    def __lt__(self, other: Kit):
        "Sortes kits by created_date"
        return self.created_date < other.created_date

    @classmethod
    def create(cls, kit_type: KitType, title: str, description: str) -> Kit:
        "Creates a Kit"
        file_name = title.replace(" ", "")

        attributes = {
            "file_name": file_name,
            "kit_type": kit_type,
            "title": title,
            "description": description,
            "image_url": cls._get_image_url(kit_type, file_name),
            "created_date": datetime.now(tz=timezone("UTC")),
        }

        return cls(**attributes)

    def to_raw_kit_dbo(self) -> KitDbo:
        "Converts a Kit to a KitDbo"
        raw_kit_dbo = KitDbo()
        raw_kit_dbo.file_name = self.file_name
        raw_kit_dbo.kit_type = self.kit_type.value
        raw_kit_dbo.title = self.title
        raw_kit_dbo.description = self.description
        raw_kit_dbo.created_date = self.created_date
        return raw_kit_dbo

    @classmethod
    def from_raw_kit_dbo(cls, raw_kit: KitDbo) -> Kit:
        "Converts a KitDbo to a Kit"
        kit_type = KitType(raw_kit.kit_type)

        return cls(
            file_name=raw_kit.file_name,
            kit_type=kit_type,
            title=raw_kit.title,
            description=raw_kit.description,
            image_url=cls._get_image_url(kit_type, raw_kit.file_name),
            created_date=raw_kit.created_date,
        )

    def to_json(self) -> Json:
        "Transforms Kit into json"
        return {
            "fileName": self.file_name,
            "kitType": self.kit_type.value,
            "title": self.title,
            "description": self.description,
            "imageUrl": self.image_url,
            "createdDate": f"{self.created_date}",
        }

    @staticmethod
    def _get_image_url(kit_type: KitType, file_name: str) -> str:
        "Generates the image url based on kit type and file name"
        return f"https://{os.environ['ASSET_BUCKET']}.s3.amazonaws.com/kits/{kit_type.value}/{file_name}/{file_name}.jpg"
