from app.calculations import add,subtract,multiply,divide, BankAccount
import pytest



@pytest.fixture
def zero_bank_account():
    return BankAccount(0)

@pytest.fixture
def initial_bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1,num2,expected", [
    (1, 2, 3),
    (5, 3, 8),
    (10, 20, 30),
    (-1, -1, -2),
])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected

def test_subtract():
    assert subtract(5,3) == 2
    
def test_multiply():
    assert multiply(9,5) == 45
    
def test_divide():  
    assert divide(15,3) == 5.0
    
def test_Bank_set_initial_balance(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_bank_default_balance(initial_bank_account):
    assert initial_bank_account.balance == 100
    
def test_withdraw(initial_bank_account):
    initial_bank_account.withdraw(20)
    assert initial_bank_account.balance == 80
    
def test_deposit(zero_bank_account):
    zero_bank_account.deposit(20)
    assert zero_bank_account.balance == 20
    
def test_collect_interest(initial_bank_account):
    initial_bank_account.collect_interest()
    assert round(initial_bank_account.balance,6) == 150
    
    
@pytest.mark.parametrize("deposited,withdrew,expected", [
    (50, 75, 75),
    (500, 30, 570),
    (25, 45, 80)
])
def test_bank_transaction(initial_bank_account,deposited, withdrew, expected):
    initial_bank_account.deposit(deposited)
    initial_bank_account.withdraw(withdrew)
    assert initial_bank_account.balance == expected
    
def test_insufficient_funds(zero_bank_account):
    with pytest.raises(ValueError):
        zero_bank_account.withdraw(100)
    