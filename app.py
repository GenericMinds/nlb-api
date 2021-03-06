from chalice import Chalice

from chalicelib.enums import KitType
from chalicelib.service.kit_service import KitService
from chalicelib.types import ApiResponse
from chalicelib.utils import get_body

app = Chalice(app_name="nlb-api")
app.debug = True


@app.route("/kits", methods=["POST"], cors=True)
def post_kit() -> ApiResponse:
    "Endpoint to post a kit"
    body = get_body(app.current_request)
    kit_post_urls = KitService.post_kit(
        title=body.get("title"),
        kit_type=KitType(body.get("kitType")),
        description=body.get("description"),
    )

    return kit_post_urls.to_json()


@app.route("/kits", methods=["GET"], cors=True)
def get_kits() -> ApiResponse:
    "Endpoint to get kits"
    kit_type = KitType.from_request(app.current_request)
    kits = KitService.get_kits(kit_type)
    jsonified_kits = [kit.to_json() for kit in kits]

    return jsonified_kits
