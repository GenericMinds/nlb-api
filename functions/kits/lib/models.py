from dataclasses import dataclass


@dataclass
class Kit:
    file_name: str
    kit_type: str
    title: str
    description: str


@dataclass
class KitUrls:
    file_name: str
    image_presigned_url: str
    zip_presigned_url: str
