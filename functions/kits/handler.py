from flask import request
from flask_lambda import FlaskLambda

from functions.kits.library.utils import response
from library.enums import KitType
from functions.kits.library.service.kit_service import KitService

app = FlaskLambda(__name__)


@app.route("/kits", methods=["POST"])
def post_kit():
    body = request.get_json()
    kit_post_urls = KitService.post_kit(
        title=body.get("title"),
        kit_type=KitType(body.get("kitType")),
        description=body.get("description"),
    )

    return response(kit_post_urls.camelize(), 201)


@app.route("/kits", methods=["GET"])
def get_kits():
    kit_type = request.args.get("kitType")
    kits = [kit.camelize() for kit in KitService.get_kits(kit_type)]

    return response(kits, 200)
