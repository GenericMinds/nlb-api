from dataclasses import dataclass
from marshmallow_dataclass import class_schema


@dataclass
class FileMetaData:
    title: str
    description: str
    file_name: str
    asset_type: str
    content_type: str


FileMetaDataSchema = class_schema(FileMetaData)


@dataclass
class FilePresignedResponse:
    asset_id: str
    presigned_url: str
