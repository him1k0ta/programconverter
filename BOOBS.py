import requests
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


# Абстрактный класс для форматирования валюты
class AbstractCurrencyFormatter(ABC):
    @abstractmethod
    def format(self, amount, currency):
        pass


# Класс для работы с API валют
class CurrencyAPI:
    def __init__(self, api_url):
        """
        Инициализация API.
        :param api_url: URL API для получения курсов валют.
        """
        self.api_url = api_url

    def get_exchange_rate(self, from_currency, to_currency):
        """
        Получает курс валюты из API.
        :from_currency: Исходная валюта (например, "USD").
        :to_currency: Целевая валюта (например, "EUR").
        :return: Курс валюты (float).
        """
        response = requests.get(f"{self.api_url}?base={from_currency}&symbols={to_currency}")
        if response.status_code == 200:
            data = response.json()
            return data['rates'][to_currency]
        else:
            raise Exception("Ошибка при запросе к API")


# Класс для кэширования курсов валют
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
        :return: Курс валюты (float).
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


# Класс для выполнения конвертации валют
class CurrencyConverter:
    def __init__(self, cache, formatter, api):
        """
        Инициализация конвертера.
        :cache: Объект CurrencyCache для получения курсов.
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
        :to_currency: Целевая валюта.
        :amount: Сумма для конвертации.
        """
        rate = self.cache.get_rate(from_currency, to_currency, self.api)  # Используем self.api
        converted_amount = amount * rate
        print(self.formatter.format(converted_amount, to_currency))


# Класс для проверки корректности введенных данных
class CurrencyValidator:
    def __init__(self, valid_currencies):
        """
        Инициализация валидатора.
        :valid_currencies: Список допустимых кодов валют (например, ["USD", "EUR"]).
        """
        self.valid_currencies = valid_currencies

    def input_currency(self, prompt):
        """
        Ввод и валидация кода валюты.
        :prompt: Подсказка для ввода (например, "Введите исходную валюту: ").
        :return: Корректный код валюты.
        """
        while True:
            currency = input(prompt).upper()
            if self.validate_currency(currency):
                return currency
            print(f"Ошибка: валюта '{currency}' не поддерживается.")

    def input_amount(self):
        """
        Ввод и валидация суммы.
        :return: Корректная сумма (float).
        """
        while True:
            try:
                amount = float(input("Введите сумму: "))
                if self.validate_amount(amount):
                    return amount
                print("Ошибка: сумма должна быть положительным числом.")
            except ValueError:
                print("Ошибка: введите числовое значение.")

    def validate_currency(self, currency):
        """
        Проверка корректности кода валюты.
        :currency: Код валюты.
        :return: True, если валюта корректна, иначе False.
        """
        return currency in self.valid_currencies

    def validate_amount(self, amount):
        """
        Проверка корректности суммы.
        :amount: Сумма.
        :return: True, если сумма корректна, иначе False.
        """
        return isinstance(amount, (int, float)) and amount > 0


# Класс для форматирования вывода
class CurrencyFormatter(AbstractCurrencyFormatter):
    def format(self, amount, currency):

        return f"Результат конвертации: {amount:.2f} {currency}"


# Класс для "красивого" форматирования вывода
class FancyCurrencyFormatter(AbstractCurrencyFormatter):
    def format(self, amount, currency):


        return f"✨ {amount:.2f} {currency} ✨"


# Главный класс, который управляет всей программой
class Main:
    def __init__(self):

        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"  # Пример API
        self.api = CurrencyAPI(self.api_url)  # Создаем объект CurrencyAPI
        self.cache = CurrencyCache()
        self.formatter = FancyCurrencyFormatter()  # Используем FancyCurrencyFormatter
        self.converter = CurrencyConverter(self.cache, self.formatter, self.api)  # Передаем api
        self.validator = CurrencyValidator(valid_currencies=["USD", "EUR", "GBP", "JPY", "RUB"])

    def run(self):

        # Ввод данных
        print("= Конвертер валют =")
        from_currency = self.validator.input_currency("Введите исходную валюту (например, USD): ")
        to_currency = self.validator.input_currency("Введите целевую валюту (например, EUR): ")
        amount = self.validator.input_amount()

        # Конвертация и вывод результата
        self.converter.convert(from_currency, to_currency, amount)


# Запуск программы
if __name__ == "__main__":
    app = Main()
    app.run()