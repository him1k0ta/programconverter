from CurrencyAPI import CurrencyAPI
from CurrencyCache import CurrencyCache
from CurrencyFormatter import CurrencyFormatter
from CurrencyConverter import CurrencyConverter
from CurrencyValidator import CurrencyValidator
class Main:
    def __init__(self):
        """
        Инициализация главного класса.
        """
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"  # Пример API
        self.api = CurrencyAPI(self.api_url)  # Создаем объект CurrencyAPI
        self.cache = CurrencyCache()
        self.formatter = CurrencyFormatter()
        self.converter = CurrencyConverter(self.cache, self.formatter, self.api)  # Передаем api
        self.validator = CurrencyValidator(valid_currencies=["USD", "EUR", "RUB"])

    def run(self):
        """
        Основной метод, который запускает программу.
        """
        # Ввод данных
        print("=== Конвертер валют ===")
        from_currency = self.validator.input_currency("Введите исходную валюту (например, USD): ")
        to_currency = self.validator.input_currency("Введите целевую валюту (например, EUR): ")
        amount = self.validator.input_amount()

        # Конвертация и вывод результата
        self.converter.convert(from_currency, to_currency, amount)

app = Main()
app.run()