import os

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class KitDbo(Model):
    "PynamoDB model to interact with DynamoDB"

    class Meta:
        table_name = os.environ["KIT_TABLE"]

    file_name = UnicodeAttribute(hash_key=True)
    kit_type = UnicodeAttribute()
    title = UnicodeAttribute()
    description = UnicodeAttribute()
