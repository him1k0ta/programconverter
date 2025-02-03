import requests
from datetime import datetime, timedelta
class CurrencyCache:
    def __init__(self):
        """
        Инициализация кэша.
        """
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Кэш актуален 1 час

    def get_rate(self, from_currency, to_currency, api):
        """
        Получает курс из кэша или API.
        :from_currency: Исходная валюта.
        :to_currency: Целевая валюта.
        :api: Объект CurrencyAPI для запроса курса, если его нет в кэше.
        :Курс валюты (float).
        """
        cache_key = f"{from_currency}_{to_currency}"
        if cache_key in self.cache:
            rate, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return rate

        # Если кэш устарел или отсутствует, запрашиваем у API
        rate = api.get_exchange_rate(from_currency, to_currency)
        self.update_cache(from_currency, to_currency, rate)
        return rate

    def update_cache(self, from_currency, to_currency, rate):
        """
        Обновляет кэш.
        :from_currency: Исходная валюта.
        :to_currency: Целевая валюта.
        :rate: Курс валюты.
        """
        cache_key = f"{from_currency}_{to_currency}"
        self.cache[cache_key] = (rate, datetime.now())