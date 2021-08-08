import ujson

from dataclasses import asdict, is_dataclass
from humps import camelize


def create_message_response(message, status: int = 200):
    body = {
        'message': message
    }

    return create_response(body, status)


def create_response(body, status: int = 200):
    body = camelize(asdict(body)) if is_dataclass(body) else body
    return {
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': status,
        'body': ujson.dumps(body),
    }
