# Класс для выполнения конвертации валют

class CurrencyConverter:
    def __init__(self, cache, formatter, api):
        """
        Инициализация конвертера.
        : cache: Объект CurrencyCache для получения курсов.
        :formatter: Объект CurrencyFormatter для форматирования результата.
        :api: Объект CurrencyAPI для запроса курсов валют.
        """
        self.cache = cache
        self.formatter = formatter
        self.api = api  # Добавляем объект CurrencyAPI

    def convert(self, from_currency, to_currency, amount):
        """
        Выполняет конвертацию и выводит результат.
        :from_currency: Исходная валюта.
        : to_currency: Целевая валюта.
        : amount: Сумма для конвертации.
        """
        rate = self.cache.get_rate(from_currency, to_currency, self.api)  # Используем self.api
        converted_amount = amount * rate
        print(self.formatter.format(converted_amount, to_currency))
