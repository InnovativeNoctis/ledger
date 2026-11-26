from decimal import Decimal

import pytest

from ledger.account import Account
from ledger.transaction import Transaction

# --- Fixtures ---------------------------------------------------------------


@pytest.fixture
def source_account() -> Account:
    return Account(name="Alice", balance=Decimal("50"), id=1)


@pytest.fixture
def destination_account() -> Account:
    return Account(name="Bob", balance=Decimal("0"), id=2)


# --- Creating an account ----------------------------------------------------


def test_account_keeps_its_name(source_account: Account) -> None:
    assert source_account.name == "Alice"


def test_account_keeps_its_balance(source_account: Account) -> None:
    assert source_account.balance == Decimal("50")


def test_account_accepts_zero_balance() -> None:
    account = Account(name="Alice", balance=Decimal("0"), id=1)
    assert account.balance == Decimal("0")


def test_account_rejects_empty_name() -> None:
    with pytest.raises(ValueError):
        Account(name="", balance=Decimal("50"), id=1)


def test_account_rejects_whitespace_only_name() -> None:
    with pytest.raises(ValueError):
        Account(name="       ", balance=Decimal("50"), id=1)


def test_account_rejects_negative_balance() -> None:
    with pytest.raises(ValueError, match="negative"):
        Account(name="Alice", balance=Decimal("-5"), id=1)


# --- Transactions list is not shared ----------------------------------------


def test_new_accounts_do_not_share_transactions() -> None:
    alice = Account("Alice", Decimal("50"), id=1)
    bob = Account("Bob", Decimal("0"), id=2)
    alice.transactions.append(Transaction("Alice", "Bob", Decimal("20")))
    assert bob.transactions == []


def test_spend_adds_transaction_to_source_only() -> None:
    alice = Account("Alice", Decimal("50"), id=1)
    bob = Account("Bob", Decimal("20"), id=2)
    alice.spend(bob, Decimal("20"))
    assert bob.transactions == []
    assert alice.transactions == [Transaction("Alice", "Bob", Decimal("20"))]


# --- Spending: success ------------------------------------------------------


def test_spend_accepts_positive_amount(
    source_account: Account, destination_account: Account
) -> None:
    source_account.spend(destination_account, Decimal("30"))
    assert source_account.balance == Decimal("20")


def test_spend_accepts_amount_equal_to_balance(
    source_account: Account, destination_account: Account
) -> None:
    source_account.spend(destination_account, Decimal("50"))
    assert source_account.balance == Decimal("0")


def test_spend_moves_money_and_adds_one_transaction() -> None:
    source = Account(name="Alice", balance=Decimal("50"), id=1)
    destination = Account(name="Bob", balance=Decimal("0"), id=2)
    source.spend(destination, Decimal("30"))
    assert source.transactions == [
        Transaction(source="Alice", destination="Bob", amount=Decimal("30"))
    ]
    assert source.balance == Decimal("20")
    assert destination.balance == Decimal("30")


def test_spend_accepts_accounts_with_the_same_name() -> None:
    source = Account(name="Alice", balance=Decimal("30"), id=1)
    destination = Account(name="Alice", balance=Decimal("22"), id=2)
    source.spend(destination, Decimal("10"))
    assert source.transactions == [
        Transaction(source.name, destination.name, Decimal("10"))
    ]
    assert source.balance == Decimal("20")
    assert destination.balance == Decimal("32")


# --- Spending: rejected -----------------------------------------------------


def test_spend_rejects_negative_amount(
    source_account: Account, destination_account: Account
) -> None:
    with pytest.raises(ValueError, match="negative"):
        source_account.spend(destination_account, Decimal("-30"))
    assert source_account.balance == Decimal("50")


def test_spend_rejects_zero_amount(
    source_account: Account, destination_account: Account
) -> None:
    with pytest.raises(ValueError, match="zero"):
        source_account.spend(destination_account, Decimal("0"))
    assert source_account.balance == Decimal("50")


def test_spend_rejects_amount_greater_than_balance(
    source_account: Account, destination_account: Account
) -> None:
    with pytest.raises(ValueError, match="greater"):
        source_account.spend(destination_account, Decimal("60"))
    assert source_account.balance == Decimal("50")


def test_spend_rejects_spending_from_zero_balance(
    destination_account: Account,
) -> None:
    source = Account(name="Carol", balance=Decimal("0"), id=3)
    with pytest.raises(ValueError, match="greater"):
        source.spend(destination_account, Decimal("1"))
    assert source.balance == Decimal("0")


def test_spend_rejects_same_source_and_destination(source_account: Account) -> None:
    with pytest.raises(ValueError, match="same"):
        source_account.spend(source_account, Decimal("20"))
    assert source_account.transactions == []
    assert source_account.balance == Decimal("50")


def test_failed_spend_changes_nothing() -> None:
    source = Account(name="Alice", balance=Decimal("30"), id=1)
    destination = Account(name="Bob", balance=Decimal("22"), id=2)
    with pytest.raises(ValueError, match="greater"):
        source.spend(destination, Decimal("50"))
    assert source.transactions == []
    assert source.balance == Decimal("30")
    assert destination.balance == Decimal("22")


# --- Spending: missing IDs --------------------------------------------------


def test_spend_rejects_source_without_id() -> None:
    source = Account(name="Alice", balance=Decimal("60"), id=None)
    destination = Account(name="Bob", balance=Decimal("20"), id=2)
    with pytest.raises(ValueError, match="Source has no ID"):
        source.spend(destination, Decimal("30"))


def test_spend_rejects_destination_without_id() -> None:
    source = Account(name="Alice", balance=Decimal("60"), id=1)
    destination = Account(name="Bob", balance=Decimal("20"), id=None)
    with pytest.raises(ValueError, match="Destination has no ID"):
        source.spend(destination, Decimal("30"))
