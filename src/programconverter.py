import sys
import logging
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QButtonGroup, QSpinBox,
    QMenuBar, QMenu, QRadioButton
)
from PyQt6.QtCore import Qt, QTranslator, QLocale
from PyQt6.QtGui import QFont, QIcon, QAction
import requests

logging.basicConfig(filename='currency_converter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class AbstractCurrencyFormatter(ABC):
    @staticmethod
    @abstractmethod
    def format(amount, currency):
        pass

class CurrencyFormatter(AbstractCurrencyFormatter):
    @staticmethod
    def format(amount, currency, decimal_places=2):
        format_str = lambda a, c, d: f"Результат конвертации: {a:.{d}f} {c}"
        logging.info(f"Форматирование результата с {decimal_places} знаками после запятой: {amount} {currency}")
        return format_str(amount, currency, decimal_places)

class FancyCurrencyFormatter(AbstractCurrencyFormatter):
    @staticmethod
    def format(amount, currency, decimal_places=2):
        format_str = lambda a, c, d: f"✨ Conversion result: {a:.{d}f} {c} ✨"
        logging.info(f"Форматирование результата English с {decimal_places} знаками после запятой: {amount} {currency}")
        return format_str(amount, currency, decimal_places)

class CurrencyAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_exchange_rate(self, from_currency, to_currency):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            return rates.get(to_currency) / rates.get(from_currency)
        return None

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

class CurrencyValidator:
    def __init__(self, valid_currencies):
        self.valid_currencies = valid_currencies

    def input_currency(self, prompt):
        while True:
            currency = input(prompt).upper()
            if self.validate_currency(currency):
                return currency
            return (f"Ошибка: валюта '{currency}' не поддерживается.")

    def input_amount(self):
        while True:
            try:
                amount = float(input("Введите сумму: "))
                if self.validate_amount(amount) and amount > 0:
                    return amount
                elif amount < 0:
                    raise ValueError("Ошибка: сумма должна быть положительным числом")
            except ValueError as e:
                return(e)
            finally:
                return("============")

    def validate_currency(self, currency):
        return currency in self.valid_currencies

    def validate_amount(self, amount):
        try:
            return isinstance(amount, (int, float))
        except ValueError:
            return("Ошибка: ваша жизнь")

class CurrencyConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.is_dark_theme = False
        self.current_language = "ru"

        self.init_ui()

        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.api = CurrencyAPI(self.api_url)
        self.cache = CurrencyCache()
        self.formatter = CurrencyFormatter()
        self.validator = CurrencyValidator(valid_currencies={"USD", "EUR", "GBP", "JPY", "RUB"})
        self.converter = CurrencyConverter(self.cache, self.formatter, self.api)

        self.apply_light_theme()
        self.retranslate_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Конвертер валют")
        self.setGeometry(100, 100, 400, 450)

        self.create_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.from_currency_label = QLabel()
        self.from_currency_input = QComboBox()
        self.from_currency_input.addItems(["USD", "EUR", "GBP", "JPY", "RUB"])
        self.layout.addWidget(self.from_currency_label)
        self.layout.addWidget(self.from_currency_input)

        self.to_currency_label = QLabel()
        self.to_currency_input = QComboBox()
        self.to_currency_input.addItems(["USD", "EUR", "GBP", "JPY", "RUB"])
        self.layout.addWidget(self.to_currency_label)
        self.layout.addWidget(self.to_currency_input)

        self.amount_label = QLabel()
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)

        self.format_label = QLabel()
        self.layout.addWidget(self.format_label)

        self.format_group = QButtonGroup()
        self.format_russian = QRadioButton()
        self.format_english = QRadioButton()
        self.format_group.addButton(self.format_russian, 1)
        self.format_group.addButton(self.format_english, 2)
        self.layout.addWidget(self.format_russian)
        self.layout.addWidget(self.format_english)

        self.decimal_label = QLabel()
        self.layout.addWidget(self.decimal_label)

        self.decimal_group = QButtonGroup()
        self.decimal_default = QRadioButton()
        self.decimal_custom = QRadioButton()
        self.decimal_group.addButton(self.decimal_default, 1)
        self.decimal_group.addButton(self.decimal_custom, 2)
        self.layout.addWidget(self.decimal_default)
        self.layout.addWidget(self.decimal_custom)

        self.custom_decimal_input = QSpinBox()
        self.custom_decimal_input.setRange(0, 10)
        self.custom_decimal_input.setValue(2)
        self.custom_decimal_input.setEnabled(False)
        self.layout.addWidget(self.custom_decimal_input)

        self.button_layout = QHBoxLayout()
        self.convert_button = QPushButton()
        self.clear_button = QPushButton()
        self.button_layout.addWidget(self.convert_button)
        self.button_layout.addWidget(self.clear_button)
        self.layout.addLayout(self.button_layout)

        self.result_label = QLabel()
        self.result_output = QLabel("")
        self.result_output.setFont(QFont("Arial", 14))
        self.result_output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.result_output)

        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_fields)
        self.decimal_custom.toggled.connect(self.toggle_custom_decimal_input)

    def create_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Настройки")

        language_menu = settings_menu.addMenu("Язык")
        self.russian_action = QAction("Русский", self)
        self.russian_action.triggered.connect(lambda: self.change_language("ru"))
        language_menu.addAction(self.russian_action)

        self.english_action = QAction("English", self)
        self.english_action.triggered.connect(lambda: self.change_language("en"))
        language_menu.addAction(self.english_action)

        theme_menu = settings_menu.addMenu("Тема")
        self.light_theme_action = QAction("Светлая", self)
        self.light_theme_action.triggered.connect(lambda: self.change_theme(False))
        theme_menu.addAction(self.light_theme_action)

        self.dark_theme_action = QAction("Темная", self)
        self.dark_theme_action.triggered.connect(lambda: self.change_theme(True))
        theme_menu.addAction(self.dark_theme_action)

    def change_language(self, language):
        if language != self.current_language:
            self.current_language = language
            if language == "en":
                self.translator.load(":/translations/english.qm")
            else:
                self.translator.load(":/translations/russian.qm")
            self.retranslate_ui()

    def retranslate_ui(self):
        if self.current_language == "en":
            self.setWindowTitle("Currency Converter")
            self.from_currency_label.setText("From currency:")
            self.to_currency_label.setText("To currency:")
            self.amount_label.setText("Amount:")
            self.format_label.setText("Select output format:")
            self.format_russian.setText("Russian")
            self.format_english.setText("English")
            self.decimal_label.setText("Select decimal places:")
            self.decimal_default.setText("Two decimal places")
            self.decimal_custom.setText("Custom decimal places")
            self.convert_button.setText("Convert")
            self.clear_button.setText("Clear")
            self.result_label.setText("Result:")

            self.menuBar().actions()[0].setText("Settings")
            self.russian_action.setText("Russian")
            self.english_action.setText("English")
            self.light_theme_action.setText("Light")
            self.dark_theme_action.setText("Dark")
        else:
            self.setWindowTitle("Конвертер валют")
            self.from_currency_label.setText("Исходная валюта:")
            self.to_currency_label.setText("Целевая валюта:")
            self.amount_label.setText("Сумма:")
            self.format_label.setText("Выберите формат вывода:")
            self.format_russian.setText("Русский")
            self.format_english.setText("English")
            self.decimal_label.setText("Выберите количество знаков после запятой:")
            self.decimal_default.setText("Два знака после запятой")
            self.decimal_custom.setText("Кастомное количество знаков")
            self.convert_button.setText("Конвертировать")
            self.clear_button.setText("Очистить")
            self.result_label.setText("Результат:")

            self.menuBar().actions()[0].setText("Настройки")
            self.russian_action.setText("Русский")
            self.english_action.setText("English")
            self.light_theme_action.setText("Светлая")
            self.dark_theme_action.setText("Темная")

    def change_theme(self, dark):
        self.is_dark_theme = dark
        if dark:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0faf0; 
            }
            QLabel {
                font-size: 14px;
                color: #333333; 
                font-family: 'Segoe UI';
            }
            QLineEdit, QComboBox, QSpinBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #a8d5a8; 
                border-radius: 10px;
                background-color: #ffffff;  
                color: #000000;  
                font-family: 'Segoe UI';
            }
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #a8d5a8;  
                color: #ffffff; 
                border: none;
                border-radius: 15px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #8cc08c; 
            }
            QRadioButton {
                font-size: 14px;
                color: #333333; 
                font-family: 'Segoe UI';
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #a8d5a8;
            }
            QRadioButton::indicator:checked {
                background-color: #a8d5a8; 
                border: 2px solid #a8d5a8;
            }
            QLabel#result_output {
                font-size: 18px;
                color: #4caf50; 
                font-family: 'Segoe UI';
            }
            QSpinBox {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QMenuBar {
                background-color: #f0faf0;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
                color: #333333;
            }
            QMenuBar::item:selected {
                background-color: #a8d5a8;
                color: #ffffff;
            }
            QMenuBar::item:hover {
                background-color: #c8e8c8;
                color: #333333;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #a8d5a8;
                color: #333333;
            }
            QMenu::item {
                padding: 5px 25px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #a8d5a8;
                color: #ffffff;
            }
            QMenu::item:hover {
                background-color: #c8e8c8;
                color: #333333;
            }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QLabel {
                font-size: 14px;
                color: #e0e0e0;
                font-family: 'Segoe UI';
            }
            QLineEdit, QComboBox, QSpinBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                background-color: #3a3a3a;
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #3a3a3a;
                color: #ffffff;
                border: none;
                border-radius: 15px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QRadioButton {
                font-size: 14px;
                color: #e0e0e0;
                font-family: 'Segoe UI';
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #4a4a4a;
            }
            QRadioButton::indicator:checked {
                background-color: #4a4a4a;
                border: 2px solid #4a4a4a;
            }
            QLabel#result_output {
                font-size: 18px;
                color: #4caf50;
                font-family: 'Segoe UI';
            }
            QSpinBox {
                background-color: #3a3a3a;
                border-radius: 10px;
            }
            QMenuBar {
                background-color: #2d2d2d;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #e0e0e0;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #3a3a3a;
            }
            QMenu {
                background-color: #3a3a3a;
                border: 1px solid #4a4a4a;
                color: #e0e0e0;
            }
            QMenu::item:selected {
                background-color: #4a4a4a;
            }
        """)

    def toggle_custom_decimal_input(self, checked):
        self.custom_decimal_input.setEnabled(checked)

    def convert_currency(self):
        try:
            from_currency = self.from_currency_input.currentText()
            to_currency = self.to_currency_input.currentText()
            amount = float(self.amount_input.text())

            if not self.validator.validate_currency(from_currency) or not self.validator.validate_currency(to_currency):
                raise ValueError("Неверная валюта" if self.current_language == "ru" else "Invalid currency")

            if not self.validator.validate_amount(amount):
                raise ValueError(
                    "Сумма должна быть положительным числом" if self.current_language == "ru" else "Amount must be positive")

            if self.format_russian.isChecked():
                self.converter.formatter = CurrencyFormatter()
            elif self.format_english.isChecked():
                self.converter.formatter = FancyCurrencyFormatter()

            if self.decimal_default.isChecked():
                decimal_places = 2
            elif self.decimal_custom.isChecked():
                decimal_places = self.custom_decimal_input.value()

            result = self.converter.convert(from_currency, to_currency, amount, decimal_places)
            self.result_output.setText(result)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка" if self.current_language == "ru" else "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка" if self.current_language == "ru" else "Error", str(e))

    def clear_fields(self):
        self.from_currency_input.setCurrentIndex(0)
        self.to_currency_input.setCurrentIndex(0)
        self.amount_input.clear()
        self.format_russian.setChecked(True)
        self.decimal_default.setChecked(True)
        self.custom_decimal_input.setValue(2)
        self.result_output.setText("")

class Main:
    def __init__(self):
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.api = CurrencyAPI(self.api_url)
        self.cache = CurrencyCache()
        self.formatter = FancyCurrencyFormatter()
        self.converter = CurrencyConverter(self.cache, self.formatter, self.api)
        self.validator = CurrencyValidator(valid_currencies={"USD": "доллар","EUR": "евро","GBP": "фунт стерлингов","JPY": "иена","RUB": "рубль"})

    def run(self):
        print("=== Конвертер валют ===")
        from_currency = self.validator.input_currency("Введите исходную валюту (например, USD): ")
        to_currency = self.validator.input_currency("Введите целевую валюту (например, EUR): ")
        amount = self.validator.input_amount()

        print("Выберите формат вывода:")
        print("1: Русский")
        print("2: English")
        choice = input("Введите номер: ")

        if choice == "1":
            self.converter.formatter = CurrencyFormatter()
        elif choice == "2":
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverterApp()
    window.show()
    sys.exit(app.exec())
    # Для консольной версии:
    # app = Main()
    # app.run()