from dataclasses import dataclass
from functions.kits.library.types import Json
from __future__ import annotations

@dataclass
class KitPostUrls:
    file_name: str
    image_presigned_url: str
    zip_presigned_url: str

    @classmethod
    def create(cls, file_name: str, image_presigned_url: str, zip_presigned_url: str) -> KitPostUrls:
        "Creates a KitPostUrls"
        attributes = {
            "file_name": file_name,
            "image_presigned_url": image_presigned_url,
            "zip_presigned_url": zip_presigned_url
        }

        return cls(**attributes)

    def to_json(self) -> Json:
        "Transforms KitPostUrls into json"
        return {
            "fileName": self.file_name,
            "imagePresignedUrl": self.image_presigned_url,
            "zipPresignedUrl": self.zip_presigned_url
        }
