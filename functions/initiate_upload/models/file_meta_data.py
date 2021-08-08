from dataclasses import dataclass


@dataclass
class FileMetaData:
    title: str
    description: str
    file_name: str
    asset_type: str
    content_type: str

    def __init__(
            self,
            title: str,
            description: str,
            fileName: str,
            assetType: str,
            contentType: str
    ) -> None:
        self.title = title
        self.description = description
        self.file_name = fileName
        self.asset_type = assetType
        self.content_type = contentType
