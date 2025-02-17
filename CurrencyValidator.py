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
        :prompt: Подсказка для ввода например, "Введите исходную валюту:.
        :return: корректный код валюты.
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

