from dataclasses import dataclass


@dataclass
class AssetMetaData:
    id: str
    title: str
    description: str
    file_name: str
    asset_type: str
    content_type: str


@dataclass
class AssetPresignedResponse:
    asset_id: str
    presigned_url: str
