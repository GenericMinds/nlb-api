import boto3
import os

from botocore.client import BaseClient


def handler(event, context):
    # Grab object details
    s3 = event['Records'][0]['s3']
    bucket_name = s3['bucket']['name']
    asset_key = s3['object']['key']

    # Grab asset metadata from s3
    s3_client: BaseClient = boto3.client('s3')
    asset = s3_client.head_object(Bucket=bucket_name, Key=asset_key)
    metadata = asset['Metadata']
    keyArray = asset_key.split('/')

    dynamodb = boto3.resource('dynamodb')

    # insert metadata into db table
    table = dynamodb.Table(os.environ['ASSET_DB_TABLE'])
    response = table.put_item(
        Item={
            "id": keyArray[1],
            "title": metadata['title'],
            "description": metadata['description'],
            "content_type": asset['ContentType'],
            "file_name": keyArray[2],
            "asset_type": keyArray[0]
        }
    )

    return response
