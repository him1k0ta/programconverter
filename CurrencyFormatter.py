from AbstractFormatter import AbstractCurrencyFormatter

class CurrencyFormatter(AbstractCurrencyFormatter):
    @staticmethod
    def format(amount, currency):
        """
        форматирует результат конвертации.
        """
        return f"Результат конвертации: {amount:.2f} {currency}"


class FancyCurrencyFormatter(AbstractCurrencyFormatter):
    @staticmethod
    def format(amount, currency):
        return f"✨ {amount:.2f} {currency} ✨"