from dataclasses import dataclass


@dataclass
class Place:
    """
    Object to represent zippopotam returned data for a zip code
    """

    place_name: str
    longitude: str
    state: str
    state_abbreviation: str
    latitude: str
