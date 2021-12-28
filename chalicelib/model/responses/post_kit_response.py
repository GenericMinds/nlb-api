from __future__ import annotations

from dataclasses import dataclass

from chalicelib.types import Json


@dataclass
class PostKitResponse:
    "Represents the response for a post kit call"

    file_name: str
    image_presigned_url: str
    zip_presigned_url: str

    @classmethod
    def create(cls, file_name: str, image_presigned_url: str, zip_presigned_url: str) -> PostKitResponse:
        "Creates a response for a post kit request. Includes presigned urls to upload kit image and zip to s3"
        attributes = {
            "file_name": file_name,
            "image_presigned_url": image_presigned_url,
            "zip_presigned_url": zip_presigned_url,
        }

        return cls(**attributes)

    def to_json(self) -> Json:
        "Returns a jsonified mapping of posted file name and presigned urls to s3"
        return {"fileName": self.file_name, "imagePresignedUrl": self.image_presigned_url, "zipPresignedUrl": self.zip_presigned_url}
