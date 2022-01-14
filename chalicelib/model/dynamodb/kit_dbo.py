import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model


class KitTypeIndex(GlobalSecondaryIndex):
    "Global secondary index based on KitType for KitDbo"

    # pylint: disable=too-few-public-methods
    class Meta:
        "Meta class to declare index settings"
        index_name = "kit-type-index"
        read_capacity_units = 0
        write_capacity_units = 0
        projection = AllProjection()

    kit_type = UnicodeAttribute(hash_key=True)


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
    kit_type_index = KitTypeIndex()
