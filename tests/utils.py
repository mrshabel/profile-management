def add(num1: int, num2: int) -> int:
    return num1 + num2


def subtract(num1: int, num2: int) -> int:
    return num1 - num2


def multiply(num1: int, num2: int) -> int:
    return num1 * num2


def divide(num1: int, num2: int) -> int:
    return num1 / num2


class BankAccount:
    """Instantiate a bank account class with balance and methods like withdraw, deposit"""

    def __init__(self, balance: float = 0.00) -> None:
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise Exception("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        """Uses an interest rate of 10%"""
        self.balance *= 1.1


class InsufficientFunds(Exception):
    pass
