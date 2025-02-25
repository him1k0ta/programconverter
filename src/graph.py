import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timedelta


# Класс для работы с API валют
class CurrencyAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_exchange_rate(self, from_currency, to_currency):
        response = requests.get(f"{self.api_url}?base={from_currency}&symbols={to_currency}")
        if response.status_code == 200:
            data = response.json()
            return data['rates'][to_currency]
        else:
            raise Exception("Ошибка при запросе к API")


# Класс для кэширования курсов валют
class CurrencyCache:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)

    def get_rate(self, from_currency, to_currency, api):
        cache_key = f"{from_currency}_{to_currency}"
        if cache_key in self.cache:
            rate, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return rate

        rate = api.get_exchange_rate(from_currency, to_currency)
        self.update_cache(from_currency, to_currency, rate)
        return rate

    def update_cache(self, from_currency, to_currency, rate):
        cache_key = f"{from_currency}_{to_currency}"
        self.cache[cache_key] = (rate, datetime.now())


# Класс для выполнения конвертации валют
class CurrencyConverter:
    def __init__(self, cache, api):
        self.cache = cache
        self.api = api

    def convert(self, from_currency, to_currency, amount):
        rate = self.cache.get_rate(from_currency, to_currency, self.api)
        converted_amount = amount * rate
        return converted_amount


# Класс для проверки корректности введенных данных
class CurrencyValidator:
    def __init__(self, valid_currencies):
        self.valid_currencies = valid_currencies

    def validate_currency(self, currency):
        return currency in self.valid_currencies

    def validate_amount(self, amount):
        return isinstance(amount, (int, float)) and amount > 0


# Класс для форматирования вывода
class CurrencyFormatter:
    def format(self, amount, currency):
        return f"Результат конвертации: {amount:.2f} {currency}"


# Главный класс, который управляет всей программой
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")

        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.api = CurrencyAPI(self.api_url)
        self.cache = CurrencyCache()
        self.converter = CurrencyConverter(self.cache, self.api)
        self.validator = CurrencyValidator(valid_currencies=["USD", "EUR", "GBP", "JPY", "RUB"])
        self.formatter = CurrencyFormatter()

        self.create_widgets()

    def create_widgets(self):
        # Ввод исходной валюты
        self.from_currency_label = tk.Label(self.root, text="Исходная валюта (например, USD):")
        self.from_currency_label.grid(row=0, column=0, padx=10, pady=10)
        self.from_currency_entry = tk.Entry(self.root)
        self.from_currency_entry.grid(row=0, column=1, padx=10, pady=10)

        # Ввод целевой валюты
        self.to_currency_label = tk.Label(self.root, text="Целевая валюта (например, EUR):")
        self.to_currency_label.grid(row=1, column=0, padx=10, pady=10)
        self.to_currency_entry = tk.Entry(self.root)
        self.to_currency_entry.grid(row=1, column=1, padx=10, pady=10)

        # Ввод суммы
        self.amount_label = tk.Label(self.root, text="Сумма:")
        self.amount_label.grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_button = tk.Button(self.root, text="Конвертировать", command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Поле для вывода результата
        self.result_label = tk.Label(self.root, text="Результат:")
        self.result_label.grid(row=4, column=0, padx=10, pady=10)
        self.result_value = tk.Label(self.root, text="")
        self.result_value.grid(row=4, column=1, padx=10, pady=10)

    def convert(self):
        from_currency = self.from_currency_entry.get().upper()
        to_currency = self.to_currency_entry.get().upper()
        amount = self.amount_entry.get()

        if not self.validator.validate_currency(from_currency):
            messagebox.showerror("Ошибка", f"Валюта '{from_currency}' не поддерживается.")
            return

        if not self.validator.validate_currency(to_currency):
            messagebox.showerror("Ошибка", f"Валюта '{to_currency}' не поддерживается.")
            return

        try:
            amount = float(amount)
            if not self.validator.validate_amount(amount):
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом.")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовое значение для суммы.")
            return

        converted_amount = self.converter.convert(from_currency, to_currency, amount)
        result_text = self.formatter.format(converted_amount, to_currency)
        self.result_value.config(text=result_text)


# Запуск программы
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()