import pytest
from src.utils import add, subtract, multiply, divide, BankAccount, InsufficientFunds


# fixture method instances the test instance of a class
@pytest.fixture
def bank_account():
    return BankAccount()


# declare bank account class
def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 20.0


@pytest.mark.parametrize(
    "deposited, withdrew, expected", [(50, 35, 15), (70, 30, 40), (1400, 1100, 300)]
)
def test_transaction(bank_account, deposited, withdrew, expected):
    bank_account.deposit(deposited)
    bank_account.withdraw(withdrew)
    assert bank_account.balance == expected


def test_insufficient_balance(bank_account):
    """Expects an exception to be thrown from the method called"""
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(10)


# assert raises error only when the value is false
@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    output = subtract(8, 2)
    assert output == 6


def test_multiply():
    output = multiply(12, 5)
    assert output == 60


def test_divide():
    output = divide(12, 4)
    assert output == 3
