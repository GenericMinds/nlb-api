from flask import request, jsonify
from flask_lambda import FlaskLambda

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

    return jsonify(kit_post_urls.camelize()), 201


@app.route("/kits", methods=["GET"])
def get_kits():
    kit_type = request.args.get("kitType")
    kits = [kit.camelize() for kit in KitService.get_kits(kit_type)]

    return jsonify(kits), 200
