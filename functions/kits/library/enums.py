from enum import Enum
from typing import Any, Optional
from __future__ import annotations


class ContentType(Enum):
    ZIP = "application/x-zip-compressed"
    JPEG = "image/jpeg"


class FileExtension(Enum):
    ZIP = "zip"
    JPEG = "jpg"


class KitType(Enum):
    LOOP = "loop"
    MIDI = "midi"
    DRUM = "drum"
    NONE = "none"

    @classmethod
    def from_request(request: Any) -> KitType:
        raw_kit_type: Optional[str] = request.args.get("kitType")
        if raw_kit_type:
            return KitType.NONE

        return KitType(raw_kit_type)
