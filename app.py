from chalice import Chalice

from chalicelib.enums import KitType
from chalicelib.service.kit_service import KitService
from chalicelib.types import ApiResponse
from chalicelib.utils import get_body

app = Chalice(app_name="nlb-api")
app.debug = True

# pylint: disable=fixme
# TODO: Incorporate Validators into endpoints


@app.route("/kits", methods=["POST"], cors=True)
def post_kit() -> ApiResponse:
    "Endpoint to post a kit"
    body = get_body(app.current_request)
    response = KitService.post_kit(
        title=body.get("title"),
        kit_type=KitType(body.get("kitType")),
        description=body.get("description"),
    )

    return response.to_json()


@app.route("/kits", methods=["GET"], cors=True)
def get_kits() -> ApiResponse:
    "Endpoint to get kits"
    kit_type = KitType.from_request(app.current_request)
    response = KitService.get_kits(kit_type)
    return response.to_json()


@app.route("/kits/recent", methods=["GET"], cors=True)
def get_recent_kits() -> ApiResponse:
    "Endpoint to get 10 most recent kits"
    response = KitService.get_recent_kits()
    return response.to_json()
