import os

from dataclasses import dataclass
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Kit(Model):
    """
    Kit PynamoDB DAO
    """
    class Meta:
        table_name = os.environ['KIT_TABLE']
    file_name = UnicodeAttribute(hash_key=True)
    kit_type = UnicodeAttribute()
    title = UnicodeAttribute()
    description = UnicodeAttribute()


@dataclass
class KitUrls:
    file_name: str
    image_presigned_url: str
    zip_presigned_url: str
