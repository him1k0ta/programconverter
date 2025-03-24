import requests
from datetime import datetime, timedelta
class CurrencyAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_exchange_rate(self, from_currency, to_currency):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            return rates.get(to_currency) / rates.get(from_currency)
        return None