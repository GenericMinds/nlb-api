import boto3
import os
import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from dataclasses import asdict
from layers.shared.common_models.asset_models import AssetMetaData


def handler(event, context):
    print(event)
    s3 = event['Records'][0]['s3']
    bucket_name = s3['bucket']['name']
    asset_key = s3['object']['key']

    asset_data = get_asset_data_from_s3(bucket_name, asset_key)
    return put_asset_data_in_dynamodb(asset_data)


def get_asset_data_from_s3(bucket_name: str, asset_key: str):
    s3_client: BaseClient = boto3.client('s3')
    try:
        asset = s3_client.head_object(Bucket=bucket_name, Key=asset_key)
    except ClientError as e:
        logging.error(e)
        raise e

    keyArray = asset_key.split('/')

    return AssetMetaData(
        id=keyArray[1],
        title=asset['Metadata']['title'],
        description=asset['Metadata']['description'],
        content_type=asset['ContentType'],
        file_name=keyArray[2],
        asset_type=keyArray[0]
    )


def put_asset_data_in_dynamodb(asset_data: AssetMetaData):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['ASSET_DB_TABLE'])
    return table.put_item(Item=asdict(asset_data))
