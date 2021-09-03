from dataclasses import dataclass


@dataclass
class KitUrls:
    file_name: str
    image_presigned_url: str
    zip_presigned_url: str
    