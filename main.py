import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import requests
from datetime import datetime, timedelta
import logging
from CurrencyAPI import CurrencyAPI
from CurrencyCache import CurrencyCache
from CurrencyFormatter import FancyCurrencyFormatter
from CurrencyConverter import CurrencyConverter
from CurrencyValidator import CurrencyValidator
from CurrencyConverterApp import CurrencyConverterApp
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
        print("=== Конвертер валют ===")
        from_currency = self.validator.input_currency("Введите исходную валюту (например, USD): ")
        to_currency = self.validator.input_currency("Введите целевую валюту (например, EUR): ")
        amount = self.validator.input_amount()

        print("Выберите формат вывода:")
        print("1: Русский")
        print("2: English")
        choice = input("Введите номер: ")

        if choice == "1":
            from CurrencyFormatter import CurrencyFormatter
            self.converter.formatter = CurrencyFormatter()
        elif choice == "2":
            from CurrencyFormatter import FancyCurrencyFormatter
            self.converter.formatter = FancyCurrencyFormatter()

        print("Выберите количество знаков после запятой:")
        print("1: Два знака после запятой")
        print("2: Кастомное количество знаков")
        decimal_choice = input("Введите номер: ")

        if decimal_choice == "1":
            decimal_places = 2
        elif decimal_choice == "2":
            decimal_places = int(input("Введите количество знаков после запятой (например, 2, 5 и т.д.): "))
        else:
            print("Неверный выбор. Используется 2 знака после запятой по умолчанию.")
            decimal_places = 2

        self.converter.convert(from_currency, to_currency, amount, decimal_places)

app = QApplication(sys.argv)
window = CurrencyConverterApp()
window.show()
sys.exit(app.exec())
#app = Main()
#app.run()