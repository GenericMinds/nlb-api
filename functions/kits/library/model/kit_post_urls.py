from dataclasses import dataclass, asdict

import humps


@dataclass
class KitPostUrls:
    file_name: str
    image_presigned_url: str
    zip_presigned_url: str

    def camelize(self):
        return humps.camelize(asdict(self))
