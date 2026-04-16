import base64
from urllib.parse import parse_qs

import requests


class Trading212Client:
    def __init__(self, api_key: str, api_secret: str):
        self.basic_auth = base64.b64encode(f"{api_key}:{api_secret}".encode('utf-8')).decode('utf-8')

    def make_request(self, path: str):
        url = f"https://live.trading212.com{path}"
        headers = {"Authorization": f"Basic {self.basic_auth}"}
        response = requests.get(url, headers=headers)
        return response

    def get_account(self):
        response = self.make_request("/api/v0/equity/account/summary")
        if response.status_code == 200:
            data = response.json()
            return data
        return {}

    def get_positions(self):
        response = self.make_request("/api/v0/equity/positions")
        if response.status_code == 200:
            data = response.json()
            return data
        return {}

    def get_dividends(self, cursor: str = ""):
        cursor_str = f"&cursor={cursor}" if cursor else ""
        response = self.make_request(f"/api/v0/equity/history/dividends?limit=50{cursor_str}")
        if response.status_code == 200:
            data = response.json()
            dividends = data.get("items", [])
            next_page_path = data.get("nextPagePath")
            if next_page_path:
                next_page_params = parse_qs(next_page_path.split("?")[1])
                next_cursor = next_page_params.get("cursor", [None])[0]
                if next_cursor:
                    next_data = self.get_dividends(next_cursor)
                    dividends.extend(next_data)
            return dividends
        return []

    def get_orders(self, cursor: str = ""):
        cursor_str = f"&cursor={cursor}" if cursor else ""
        response = self.make_request(f"/api/v0/equity/history/orders?limit=50{cursor_str}")
        if response.status_code == 200:
            data = response.json()
            orders = data.get("items", [])
            next_page_path = data.get("nextPagePath")
            if next_page_path:
                next_page_params = parse_qs(next_page_path.split("?")[1])
                next_cursor = next_page_params.get("cursor", [None])[0]
                if next_cursor:
                    next_data = self.get_orders(next_cursor)
                    orders.extend(next_data)
            return orders
        return []

    def get_transactions(self, cursor: str = ""):
        cursor_str = f"&cursor={cursor}" if cursor else ""
        response = self.make_request(f"/api/v0/equity/history/transactions?limit=50{cursor_str}")
        if response.status_code == 200:
            data = response.json()
            transactions = data.get("items", [])
            next_page_path = data.get("nextPagePath")
            if next_page_path:
                next_page_params = parse_qs(next_page_path.split("?")[1])
                next_cursor = next_page_params.get("cursor", [None])[0]
                if next_cursor:
                    next_data = self.get_transactions(next_cursor)
                    transactions.extend(next_data)
            return transactions
        return []
