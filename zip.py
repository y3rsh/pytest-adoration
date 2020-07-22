import logging
import json
from dataclasses import dataclass
from dataclasses import field
from typing import List
from place import Place

logger = logging.getLogger(__name__)


@dataclass
class Zip:
    post_code: str = None
    country: str = None
    country_abbreviation: str = None
    places: List[Place] = field(default_factory=list)

    def safe_load(self, body):
        try:
            zip_holder = json.loads(body)
            self.post_code = zip_holder["post code"]
            self.country = zip_holder["country"]
            self.country_abbreviation = zip_holder["country abbreviation"]
            for place in zip_holder["places"]:
                self.places.append(
                    Place(
                        place_name=place["place name"],
                        longitude=place["longitude"],
                        state=place["state"],
                        state_abbreviation=place["state abbreviation"],
                        latitude=place["latitude"],
                    )
                )
        except KeyError as e:
            logger.exception(f"Key {e} NOT FOUND")
