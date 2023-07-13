import pytest
from app.calculations import add, BankAccount, InsufficientFund

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 5 , 17)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected 

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_fund(bank_account):
    with pytest.raises(InsufficientFund):
        bank_account.withdraw(200)
