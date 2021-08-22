from dataclasses import dataclass


@dataclass
class Kit:
    file_name: str
    kit_type: str
    title: str
    description: str


@dataclass
class KitPresignedResponse:
    file_name: str
    presigned_url: str
