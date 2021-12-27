from flask import request
from flask_lambda import FlaskLambda
from library.enums import KitType

from functions.kits.library.service.kit_service import KitService
from functions.kits.library.utils import response

app = FlaskLambda(__name__)


@app.route("/kits", methods=["POST"])
def post_kit():
    body = request.get_json()
    kit_post_urls = KitService.post_kit(
        title=body.get("title"),
        kit_type=KitType(body.get("kitType")),
        description=body.get("description"),
    )

    return response(kit_post_urls.to_json(), 201)


@app.route("/kits", methods=["GET"])
def get_kits():
    kit_type = KitType.from_request(request)
    jsonified_kits = [kit.to_json() for kit in KitService.get_kits(kit_type)]

    return response(jsonified_kits, 200)
