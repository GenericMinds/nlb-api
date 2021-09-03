import humps

from flask import request, jsonify
from flask_lambda import FlaskLambda
from dataclasses import asdict

from library.enums import KitType
from functions.kits.library.service.kit_service import KitService

app = FlaskLambda(__name__)


@app.route('/kits', methods=['POST'])
def post_kit():
    body = humps.decamelize(request.get_json())
    response = KitService.post_kit(**body, kit_type=KitType(body.get("kit_type")))
    return jsonify(humps.camelize(asdict(response))), 201


@app.route('/kits', methods=['GET'])
def get_kits():
    kit_type = request.args.get('kitType')
    response = KitService.get_kits(kit_type)
    return jsonify(humps.camelize(response)), 200
