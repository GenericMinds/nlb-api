from typing import Mapping
from chalice.app import Request
from chalicelib.types import Json

def get_query_params(request: Request) -> Mapping[str, str]:
    "Gets any query params passed to Chalice's base request"
    return request.query_params if request.query_params else {}


def get_body(request: Request) -> Json:
    "Gets jsonified body data passed to Chalice's base request"
    return request.json_body
