from dataclasses import dataclass


@dataclass
class FilePresignedResponse:
    asset_id: str
    presigned_url: str
