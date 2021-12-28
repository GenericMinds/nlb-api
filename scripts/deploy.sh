#!/bin/bash

# Convets Pipfile to requirements.txt
pipenv lock --requirements > requirements.txt

# Generates S3 bucket and DynamoDB table
aws cloudformation deploy --template-file template.yaml --stack-name nlb-api --capabilities CAPABILITY_IAM

# Generates Chalice Lambda
chalice deploy