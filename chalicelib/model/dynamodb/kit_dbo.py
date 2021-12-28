import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class KitDbo(Model):
    "PynamoDB model to interact with DynamoDB"

    # pylint: disable=too-few-public-methods
    class Meta:
        "Meta class to set table name"
        table_name = os.environ["KIT_TABLE"]

    file_name = UnicodeAttribute(hash_key=True)
    kit_type = UnicodeAttribute()
    title = UnicodeAttribute()
    description = UnicodeAttribute()
    created_date = UTCDateTimeAttribute()
