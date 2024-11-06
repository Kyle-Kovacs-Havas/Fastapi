import pytest
from app.calculations import add, subtract, BankAccount, InsufficentFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (2,5,7), 
    (5,5,10)
])
def test_add(num1,num2,expected):
    print("Testing add function")
    assert add(num1,num2) == expected

def test_subtract():
    print("Testing subtract function")
    assert subtract(5,5) == 0




def test_Bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_Bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100), 
    (50,5,45),
    (1200,200,1000)
])
def test_bank_transaction(zero_bank_account,deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficent_funds(zero_bank_account):
    with pytest.raises(InsufficentFunds):
        zero_bank_account.withdraw(10)
