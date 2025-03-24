import logging
from AbstractFormatter import AbstractCurrencyFormatter
logging.basicConfig(filename='currency_converter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
class CurrencyFormatter(AbstractCurrencyFormatter):
    @staticmethod
    def format(amount, currency):
        """
        форматирует результат конвертации.
        """
        format_str = lambda a, c: f"Результат конвертации: {a:.2f} {c}"
        logging.info(f"Форматирование результата: {amount} {currency}")
        return format_str(amount, currency)

    @staticmethod
    def format(amount, currency, decimal_places=2):
        format_str = lambda a, c, d: f"Результат конвертации: {a:.{d}f} {c}"
        logging.info(f"Форматирование результата с {decimal_places} знаками после запятой: {amount} {currency}")
        return format_str(amount, currency, decimal_places)

class FancyCurrencyFormatter(AbstractCurrencyFormatter):
    @staticmethod
    def format(amount, currency):
        format_str = lambda a, c: f"✨ Conversion result: {a:.2f} {c} ✨"
        logging.info(f"Форматирование результата English: {amount} {currency}")
        return format_str(amount, currency)

    @staticmethod
    def format(amount, currency, decimal_places=2):
        format_str = lambda a, c, d: f"✨ Conversion result: {a:.{d}f} {c} ✨"
        logging.info(f"Форматирование результата English с {decimal_places} знаками после запятой: {amount} {currency}")
        return format_str(amount, currency, decimal_places)