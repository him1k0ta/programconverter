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
            return (f"Ошибка: валюта '{currency}' не поддерживается.")

    def input_amount(self):
        """
        Ввод и валидация суммы.
        :return: Корректная сумма (float).
        """
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
        try:
            return isinstance(amount, (int, float))
        except ValueError:
            return("Ошибка: ваша жизнь")
