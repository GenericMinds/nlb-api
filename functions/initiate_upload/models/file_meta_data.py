from dataclasses import dataclass


@dataclass
class FileMetaData:
    title: str
    description: str
    file_name: str
    asset_type: str
    content_type: str
