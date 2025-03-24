import logging

logging.basicConfig(filename='currency_converter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CurrencyConverter:
    def __init__(self, cache, formatter, api):
        self.cache = cache
        self.formatter = formatter
        self.api = api
        logging.info(f"Инициализация CurrencyConverter с форматтером: {formatter.__class__.__name__}")

    def convert(self, from_currency, to_currency, amount, decimal_places=2):
        logging.info(f"Конвертация: {amount} {from_currency} -> {to_currency} с {decimal_places} знаками после запятой")
        rate = self.cache.get_rate(from_currency, to_currency, self.api)
        logging.info(f"Курс обмена: {rate}")
        converted_amount = amount * rate
        logging.info(f"Результат конвертации до форматирования: {converted_amount} {to_currency}")
        result = self.formatter.format(converted_amount, to_currency, decimal_places)
        logging.info(f"Форматированный результат: {result}")
        return result