import requests

HEADERS = {"Accept": "application/json", "Content-type": "application/json"}


class ZippopotamClient:  # pylint: disable=too-few-public-methods
    """
    client for the zippopotam rest api
    """

    def __init__(self, base_url):
        self.base_url = f"http://{base_url}"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_us_by_zip(self, zip_code: str):
        """
        retrieve place data for the united states (us) by zip code
        """
        endpoint = f"{self.base_url}/us/{zip_code}"
        return self.session.get(endpoint, timeout=5)
