import boto3
import os

from botocore.client import BaseClient


def handler(event, context):
    s3_client: BaseClient = boto3.client('s3')

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    print(bucket)
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(os.environ['ASSET_DB_TABLE'])
    response = table.put_item(
        Item={
            "title": "Test Title",
            "description": "These beats are on fire",
            "content_type": "application/zip",
            "file_name": "beatSauce.zip",
            "asset_type": "kits"
        }
    )

    return response
