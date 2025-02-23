from CurrencyAPI import CurrencyAPI
from CurrencyCache import CurrencyCache
from CurrencyFormatter import FancyCurrencyFormatter
from CurrencyConverter import CurrencyConverter
from CurrencyValidator import CurrencyValidator

class Main:
    def __init__(self):
        """
        Инициализация главного класса.
        """
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.api = CurrencyAPI(self.api_url)  # Создаем объект CurrencyAPI
        self.cache = CurrencyCache()
        self.formatter = FancyCurrencyFormatter()
        self.converter = CurrencyConverter(self.cache, self.formatter, self.api)  # Передаем api
        self.validator = CurrencyValidator(valid_currencies={"USD": "доллар","EUR": "евро","GBP": "фунт стерлингов","JPY": "иена","RUB": "рубль"})

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
