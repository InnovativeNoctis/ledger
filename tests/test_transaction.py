from decimal import Decimal

import pytest

from ledger.transaction import Transaction


@pytest.fixture
def transaction():
    return Transaction(source="Salary", destination="Bank", amount=Decimal("5.02"))


def test_transaction_keeps_its_source(transaction):
    assert transaction.source == "Salary"


def test_transaction_keeps_its_destination(transaction):
    assert transaction.destination == "Bank"


def test_transaction_keeps_its_amount(transaction):
    assert transaction.amount == Decimal("5.02")


def test_transaction_rejects_empty_source():
    with pytest.raises(ValueError):
        Transaction(source="", destination="Bank", amount=Decimal("5.02"))


def test_transaction_rejects_empty_destination():
    with pytest.raises(ValueError):
        Transaction(source="Salary", destination="", amount=Decimal("5.02"))


def test_transaction_rejects_whitespaces_only_source():
    with pytest.raises(ValueError):
        Transaction(source="       ", destination="Bank", amount=Decimal("5.02"))


def test_transaction_rejects_whitespaces_only_destination():
    with pytest.raises(ValueError):
        Transaction(source="Salary", destination="      ", amount=Decimal("5.02"))


def test_transaction_rejects_negative_amount():
    with pytest.raises(ValueError):
        Transaction(source="Salary", destination="Bank", amount=Decimal("-5"))


def test_transaction_rejects_zero_amount():
    with pytest.raises(ValueError):
        Transaction(source="Salary", destination="Bank", amount=Decimal("0"))
