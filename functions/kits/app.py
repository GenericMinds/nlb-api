import humps

from flask import request, jsonify
from flask_lambda import FlaskLambda
from dataclasses import asdict

from library.enums import ContentType
from library.kit_service import KitService
from library.models import Kit, KitUrls

app = FlaskLambda(__name__)


@app.route('/kits', methods=['POST'])
def kits_post():
    body = humps.decamelize(request.get_json())

    kit = Kit(**body, file_name=body['title'].replace(" ", ""))
    kit.save()

    kitUrls = KitUrls(
        file_name=kit.file_name,
        image_presigned_url=KitService.generate_put_presigned_url(kit, ContentType.JPEG),
        zip_presigned_url=KitService.generate_put_presigned_url(kit, ContentType.ZIP)
    )

    return jsonify(humps.camelize(asdict(kitUrls))), 201


@app.route('/kits', methods=['GET'])
def kits_get():
    kit_type = request.args.get('kitType')
    if kit_type:
        filter_condition = Kit.kit_type == kit_type
    else:
        filter_condition = None

    iterable_kits = Kit.scan(filter_condition=filter_condition)
    kits = [
        kit.attribute_values
        for kit in iterable_kits
    ]

    return jsonify(humps.camelize(kits)), 200
