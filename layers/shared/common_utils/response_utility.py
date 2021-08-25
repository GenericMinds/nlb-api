import ujson

from dataclasses import asdict, is_dataclass
from humps import camelize


class ResponseUtility:

    @staticmethod
    def create_message_response(message, status: int = 200):
        body = {
            'message': message
        }

        return ResponseUtility.create_response(body, status)

    @staticmethod
    def create_response(body, status: int = 200):
        body = asdict(body) if is_dataclass(body) else body
        return {
            'headers': {
                'Content-Type': 'application/json'
            },
            'statusCode': status,
            'body': ujson.dumps(camelize(body)),
        }
