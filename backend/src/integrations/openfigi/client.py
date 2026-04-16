import requests


class OpenFIGIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def make_request(self, path: str):
        url = f"https://api.openfigi.com{path}"
        headers = {
            "Content-Type": "application/json",
            "X-OPENFIGI-APIKEY": self.api_key
        }
        response = requests.get(url, headers=headers)
        return response

    def get_isin_mapping(self, isin: str):
        response = self.make_request(f"/v3/mapping/ID_ISIN/{isin}")
        if response.status_code == 200:
            data = response.json()
            return data
        return {}

    def pick_primary_isin_mapping(self, results: list):
        for r in results:
            if r.get("securityType") == "Common Stock":
                return r
        return None
