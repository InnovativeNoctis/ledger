from decimal import Decimal

from ledger.transaction import Transaction


class Account:
    def __init__(self, name, balance, transactions=None) -> None:
        if not name.strip():
            raise ValueError("Name can't be empty or whitespaces only.")
        if balance < Decimal(0):
            raise ValueError("Balance can't be negative.")
        if transactions is None:
            transactions = []

        self.name: str = name
        self.balance: Decimal = balance
        self.transactions = transactions

    def spend(self, destination, amount) -> None:
        if self is destination:
            raise ValueError("Source and Destination can't be the same.")
        if amount == 0:
            raise ValueError("The spending amount can't be zero.")
        if amount < 0:
            raise ValueError("The spending amount can't be negative.")
        if self.balance < amount:
            raise ValueError("The spending amount can't be greater than balance.")
        transaction = Transaction(
            source=self.name, destination=destination.name, amount=amount
        )
        self.balance -= amount
        destination.balance += amount
        self.transactions.append(transaction)
