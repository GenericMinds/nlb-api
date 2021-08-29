import humps

from flask import request, jsonify
from flask_lambda import FlaskLambda
from dataclasses import asdict

from lib.enums import ContentType
from lib.kit_service import KitService
from lib.models import Kit

app = FlaskLambda(__name__)


@app.route('/kits', methods=['POST'])
def lambda_handler():
    body = humps.decamelize(request.get_json())
    kit = Kit(**body, file_name=body['title'].replace(" ", ""))
    KitService.put_kit_in_dynamodb(kit)

    jpeg_presigned_url = KitService.generate_put_presigned_url(kit, ContentType.JPEG)
    zip_presigned_url = KitService.generate_put_presigned_url(kit, ContentType.ZIP)

    result = [
        humps.camelize(asdict(jpeg_presigned_url)),
        humps.camelize(asdict(zip_presigned_url))
    ]

    return jsonify(result), 201
