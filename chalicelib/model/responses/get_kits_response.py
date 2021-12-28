from __future__ import annotations

from dataclasses import dataclass
from typing import List

from chalicelib.model.kit import Kit
from chalicelib.types import Json


@dataclass
class GetKitsResponse:
    "Represents the response for a get kits call"

    kits: List[Kit]

    @classmethod
    def create(cls, kits: List[Kit]) -> GetKitsResponse:
        "Creates a response for a get kits call"
        attributes = {"kits": kits}
        return cls(**attributes)

    def to_json(self) -> Json:
        "Returns a jsonified list of kits"
        jsonified_kits = [kit.to_json() for kit in self.kits]
        return jsonified_kits
