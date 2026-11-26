from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    source: str
    destination: str
    amount: Decimal

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Source can't be empty.")
        if not self.destination.strip():
            raise ValueError("Destination can't be empty.")
        if self.amount <= Decimal("0"):
            raise ValueError("Amount can't be smaller or equal to zero.")
