# Helper function to return a response with status code and CORS headers
from typing import Any, Tuple
import flask


def response(data: Any, status_code: int) -> Tuple[Any, int]:
    result = flask.jsonify(data)
    result.headers.set('Access-Control-Allow-Origin', '*')
    result.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT')
    return result, status_code
