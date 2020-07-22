import requests

HEADERS = {"Accept": "application/json", "Content-type": "application/json"}


class ZippopotamClient:
    def __init__(self, base_url):
        self.base_url = f"http://{base_url}"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_us_by_zip(self, zip: str):
        endpoint = f"{self.base_url}/us/{zip}"
        return self.session.get(endpoint, timeout=5)
