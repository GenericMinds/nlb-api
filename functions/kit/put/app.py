import boto3
import os
import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from dataclasses import asdict
from layers.shared.common_models.kit_models import Kit


def handler(event, context):
    s3 = event['Records'][0]['s3']
    bucket_name = s3['bucket']['name']
    kit_key = s3['object']['key']

    asset_data = get_kit_from_s3(bucket_name, kit_key)
    return put_kit_in_dynamodb(asset_data)


def get_kit_from_s3(bucket_name: str, kit_key: str) -> Kit:
    s3_client: BaseClient = boto3.client('s3')
    try:
        kit = s3_client.head_object(Bucket=bucket_name, Key=kit_key)
    except ClientError as e:
        logging.error(e)
        raise e

    keyArray = kit_key.split('/')

    return Kit(
        file_name=keyArray[2],
        kit_type=keyArray[1],
        title=kit['Metadata']['title'],
        description=kit['Metadata']['description'],
    )


def put_kit_in_dynamodb(kit: Kit):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['KIT_TABLE'])
    return table.put_item(Item=asdict(kit))
