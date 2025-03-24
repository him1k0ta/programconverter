import sys
from PyQt6.QtWidgets import (
    QRadioButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox,
    QButtonGroup,QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import requests
from datetime import datetime, timedelta

from PyQt6.QtGui import QFont, QIcon
from CurrencyAPI import CurrencyAPI
from CurrencyCache import CurrencyCache
from CurrencyFormatter import CurrencyFormatter, FancyCurrencyFormatter
from CurrencyConverter import CurrencyConverter
from CurrencyValidator import CurrencyValidator

class CurrencyConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка основного окна
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Конвертер валют")
        self.setGeometry(100, 100, 400, 400)

        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        self.layout = QVBoxLayout(self.central_widget)

        # Поле для ввода исходной валюты
        self.from_currency_label = QLabel("Исходная валюта:")
        self.from_currency_input = QComboBox()
        self.from_currency_input.addItems(["USD", "EUR", "GBP", "JPY", "RUB"])
        self.layout.addWidget(self.from_currency_label)
        self.layout.addWidget(self.from_currency_input)

        # Поле для ввода целевой валюты
        self.to_currency_label = QLabel("Целевая валюта:")
        self.to_currency_input = QComboBox()
        self.to_currency_input.addItems(["USD", "EUR", "GBP", "JPY", "RUB"])
        self.layout.addWidget(self.to_currency_label)
        self.layout.addWidget(self.to_currency_input)

        # Поле для ввода суммы
        self.amount_label = QLabel("Сумма:")
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)

        # Выбор формата вывода
        self.format_label = QLabel("Выберите формат вывода:")
        self.layout.addWidget(self.format_label)

        self.format_group = QButtonGroup()
        self.format_russian = QRadioButton("Русский")
        self.format_english = QRadioButton("English")
        self.format_group.addButton(self.format_russian, 1)
        self.format_group.addButton(self.format_english, 2)
        self.layout.addWidget(self.format_russian)
        self.layout.addWidget(self.format_english)

        # Выбор количества знаков после запятой
        self.decimal_label = QLabel("Выберите количество знаков после запятой:")
        self.layout.addWidget(self.decimal_label)

        self.decimal_group = QButtonGroup()
        self.decimal_default = QRadioButton("Два знака после запятой")
        self.decimal_custom = QRadioButton("Кастомное количество знаков")
        self.decimal_group.addButton(self.decimal_default, 1)
        self.decimal_group.addButton(self.decimal_custom, 2)
        self.layout.addWidget(self.decimal_default)
        self.layout.addWidget(self.decimal_custom)

        self.custom_decimal_input = QSpinBox()
        self.custom_decimal_input.setRange(0, 10)
        self.custom_decimal_input.setValue(2)
        self.custom_decimal_input.setEnabled(False)
        self.layout.addWidget(self.custom_decimal_input)

        # Кнопки
        self.button_layout = QHBoxLayout()
        self.convert_button = QPushButton("Конвертировать")
        self.clear_button = QPushButton("Очистить")
        self.button_layout.addWidget(self.convert_button)
        self.button_layout.addWidget(self.clear_button)
        self.layout.addLayout(self.button_layout)

        # Поле для вывода результата
        self.result_label = QLabel("Результат:")
        self.result_output = QLabel("")
        self.result_output.setFont(QFont("Arial", 14))
        self.result_output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.result_output)
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
                """)
        # Инициализация классов
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.api = CurrencyAPI(self.api_url)
        self.cache = CurrencyCache()
        self.formatter = CurrencyFormatter()
        self.validator = CurrencyValidator(valid_currencies={"USD", "EUR", "GBP", "JPY", "RUB"})
        self.converter = CurrencyConverter(self.cache, self.formatter, self.api)

        # Подключение кнопок к методам
        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_fields)
        self.decimal_custom.toggled.connect(self.toggle_custom_decimal_input)

    def toggle_custom_decimal_input(self, checked):
        """
        Включает или отключает поле для ввода кастомного количества знаков после запятой.
        """
        self.custom_decimal_input.setEnabled(checked)

    def convert_currency(self):
        """
        Метод для конвертации валюты.
        """
        try:
            from_currency = self.from_currency_input.currentText()
            to_currency = self.to_currency_input.currentText()
            amount = float(self.amount_input.text())

            if not self.validator.validate_currency(from_currency) or not self.validator.validate_currency(to_currency):
                raise ValueError("Неверная валюта")

            if not self.validator.validate_amount(amount):
                raise ValueError("Сумма должна быть положительным числом")

            # Выбор формата вывода
            if self.format_russian.isChecked():
                self.converter.formatter = CurrencyFormatter()
            elif self.format_english.isChecked():
                self.converter.formatter = FancyCurrencyFormatter()

            # Выбор количества знаков после запятой
            if self.decimal_default.isChecked():
                decimal_places = 2
            elif self.decimal_custom.isChecked():
                decimal_places = self.custom_decimal_input.value()

            result = self.converter.convert(from_currency, to_currency, amount, decimal_places)
            self.result_output.setText(result)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def clear_fields(self):
        """
        Метод для очистки полей.
        """
        self.from_currency_input.setCurrentIndex(0)
        self.to_currency_input.setCurrentIndex(0)
        self.amount_input.clear()
        self.format_russian.setChecked(True)
        self.decimal_default.setChecked(True)
        self.custom_decimal_input.setValue(2)
        self.result_output.setText("")