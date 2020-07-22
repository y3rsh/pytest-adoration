from dataclasses import dataclass


@dataclass
class Place:
    place_name: str
    longitude: str
    state: str
    state_abbreviation: str
    latitude: str
