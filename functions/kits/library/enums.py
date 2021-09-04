from enum import Enum


class ContentType(Enum):
    ZIP = "application/zip"
    JPEG = "image/jpeg"


class FileExtension(Enum):
    ZIP = "zip"
    JPEG = "jpg"


class KitType(str, Enum):
    LOOP = "loop"
    MIDI = "midi"
    DRUM = "drum"
