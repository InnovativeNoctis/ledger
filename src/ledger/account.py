from decimal import Decimal


class Account:
    def __init__(self, name, balance) -> None:
        self.name: str = name
        self.balance: Decimal = balance
        if not self.name.strip():
            raise ValueError("Name can't be empty or whitespaces only.")
        if self.balance < Decimal(0):
            raise ValueError("Balance can't be negative.")

    def spend(self, amount: Decimal) -> None:
        if amount == 0:
            raise ValueError("The spending amount can't be zero.")
        if amount < 0:
            raise ValueError("The spending amount can't be negative.")
        if self.balance < amount:
            raise ValueError("The spending amount can't be greater than balance.")

        self.balance = self.balance - amount
