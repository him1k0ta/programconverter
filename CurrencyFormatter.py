# Класс для форматирования вывода
class CurrencyFormatter:
    def format(self, amount, currency):
        """
        Форматирует результат конвертации.
        :amount: Сумма.
        :currency: Код валюты.
        :return: Отформатированная строка.
        """
        return f"Результат конвертации: {amount:.2f} {currency}"
