import humps

from flask import request, jsonify
from flask_lambda import FlaskLambda
from dataclasses import asdict

from lib.enums import ContentType
from lib.kit_service import KitService
from lib.models import Kit, KitUrls

app = FlaskLambda(__name__)


@app.route('/kits', methods=['POST'])
def lambda_handler():
    body = humps.decamelize(request.get_json())

    kit = Kit(**body, file_name=body['title'].replace(" ", ""))
    KitService.put_kit_in_dynamodb(kit)

    kitUrls = KitUrls(
        file_name=kit.file_name,
        image_presigned_url=KitService.generate_put_presigned_url(kit, ContentType.JPEG),
        zip_presigned_url=KitService.generate_put_presigned_url(kit, ContentType.ZIP)
    )

    return jsonify(humps.camelize(asdict(kitUrls))), 201
