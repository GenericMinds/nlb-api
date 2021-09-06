from enum import Enum


class ContentType(Enum):
    ZIP = "application/x-zip-compressed"
    JPEG = "image/jpeg"


class FileExtension(Enum):
    ZIP = "zip"
    JPEG = "jpg"


class KitType(str, Enum):
    LOOP = "loop"
    MIDI = "midi"
    DRUM = "drum"
