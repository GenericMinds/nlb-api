import json


def create_message_response(message, status: int = 200):
    body = {
        'message': message
    }

    return create_response(body, status)


def create_response(body, status: int = 200):
    return {
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': status,
        'body': json.dumps(body),
    }