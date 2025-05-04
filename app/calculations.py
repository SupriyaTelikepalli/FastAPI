def add(num1: int, num2: 2):
    """
    Adds two numbers and returns the result.
    
    Args:
        num1 (int): The first number.
        num2 (int): The second number.
        
    Returns:
        int: The sum of num1 and num2.
    """
    return num1 + num2
    
def subtract(num1: int, num2: int):
    """
    Subtracts num2 from num1 and returns the result.
    
    Args:
        num1 (int): The first number.
        num2 (int): The second number.
        
    Returns:
        int: The difference of num1 and num2.
    """
    return num1 - num2

def multiply(num1: int, num2: int):
    """
    Multiplies two numbers and returns the result.
    
    Args:
        num1 (int): The first number.
        num2 (int): The second number.
        
    Returns:
        int: The product of num1 and num2.
    """
    return num1 * num2

def divide(num1: int, num2: int):
    """
    Divides num1 by num2 and returns the result.
    
    Args:
        num1 (int): The first number.
        num2 (int): The second number.
        
    Returns:
        float: The quotient of num1 and num2.
        
    Raises:
        ValueError: If num2 is zero.
    """
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2

class BankAccount:
    """
    A simple bank account class.
    
    Attributes:
        balance (float): The current balance of the account.
    """
    
    def __init__(self, initial_balance: float = 0.0):
        self.balance = initial_balance
        
    def deposit(self, amount: float):
        """
        Deposits a specified amount into the account.
        
        Args:
            amount (float): The amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        
    def withdraw(self, amount: float):
        """
        Withdraws a specified amount from the account.
        
        Args:
            amount (float): The amount to withdraw.
            
        Raises:
            ValueError: If the withdrawal amount exceeds the balance.
        """
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        
    def get_balance(self) -> float:
        """
        Returns the current balance of the account.
        
        Returns:
            float: The current balance.
        """
        return self.balance
    def collect_interest(self):
        """
        Collects interest on the current balance.
        
        Args:
            rate (float): The interest rate as a decimal (e.g., 0.05 for 5%).
        """
        self.balance = self.balance * 1.5