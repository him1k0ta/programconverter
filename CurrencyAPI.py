import requests
from datetime import datetime, timedelta

class CurrencyAPI:
    def __init__(self, api_url):
        """
        Инициализация API.
        : URL API для получения курсов валют.
        """
        self.api_url = api_url

    def get_exchange_rate(self, from_currency, to_currency):
        """
        Получает курс валюты из API.
        :Исходная валюта (например, "USD").
        :Целевая валюта (например, "EUR").
        :Курс валюты (float).
        """
        response = requests.get(f"{self.api_url}?base={from_currency}&symbols={to_currency}")
        if response.status_code == 200:
            data = response.json()
            return data['rates'][to_currency]
        else:
            raise Exception("Ошибка при запросе к API")