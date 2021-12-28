from __future__ import annotations

from enum import Enum
from typing import Optional

from chalice.app import Request

from chalicelib.utils import get_query_params


class ContentType(Enum):
    "Represents content types"
    ZIP = "application/x-zip-compressed"
    JPEG = "image/jpeg"


class FileExtension(Enum):
    "Represents file extensions"
    ZIP = "zip"
    JPEG = "jpg"


class KitType(Enum):
    "Represents kit types"
    LOOP = "loop"
    MIDI = "midi"
    DRUM = "drum"
    NONE = "none"

    @classmethod
    def from_request(cls, request: Request) -> KitType:
        "Creates a new kit type from request"
        raw_kit_type: Optional[str] = get_query_params(request).get("kitType")
        if not raw_kit_type:
            return cls.NONE

        return cls(raw_kit_type)
