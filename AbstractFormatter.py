from abc import ABC, abstractmethod

class AbstractCurrencyFormatter(ABC):
    @staticmethod
    @abstractmethod
    def format(amount, currency):
        pass

