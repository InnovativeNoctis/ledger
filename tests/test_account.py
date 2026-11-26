from decimal import Decimal

import pytest

from ledger.account import Account
from ledger.transaction import Transaction


@pytest.fixture
def account() -> Account:
    return Account(name="Sam Sepiol", balance=Decimal("50"))


@pytest.fixture
def other() -> Account:
    return Account(name="Umbrella", balance=Decimal("0"))


def test_account_keeps_its_name(account: Account) -> None:
    assert account.name == "Sam Sepiol"


def test_account_rejects_whitespaces_only_name() -> None:
    with pytest.raises(ValueError):
        Account(name="       ", balance=Decimal("50"))


def test_account_keeps_its_balance(account: Account) -> None:
    assert account.balance == Decimal("50")


def test_two_accounts_do_not_share_transactions() -> None:
    first = Account("Sam Sepiol", Decimal(50))
    second = Account("Sharon Dune", Decimal(0))
    first.transactions.append(Transaction("Sam Sepiol", "Just test", Decimal("20")))
    assert second.transactions == []


def test_account_rejects_empty_name() -> None:
    with pytest.raises(ValueError):
        Account(name="", balance=Decimal("50"))


def test_account_rejects_negative_balance() -> None:
    with pytest.raises(ValueError, match="negative"):
        Account(name="Sam Sepiol", balance=Decimal("-5"))


def test_account_accepts_spending_with_positive_number(
    account: Account, other: Account
) -> None:
    account.spend(other, Decimal("30"))
    assert account.balance == Decimal("20")


def test_account_accepts_spending_equal_to_balance(
    account: Account, other: Account
) -> None:
    account.spend(other, Decimal("50"))
    assert account.balance == Decimal("0")


def test_account_rejects_spending_with_negative_number(
    account: Account, other: Account
) -> None:
    with pytest.raises(ValueError, match="negative"):
        account.spend(other, Decimal("-30"))
    assert account.balance == Decimal("50")


def test_account_rejects_spending_with_zero_number(
    account: Account, other: Account
) -> None:
    with pytest.raises(ValueError, match="zero"):
        account.spend(other, Decimal("0"))
    assert account.balance == Decimal("50")


def test_account_rejects_spending_more_than_balance(
    account: Account, other: Account
) -> None:
    with pytest.raises(ValueError, match="greater"):
        account.spend(other, Decimal("60"))
    assert account.balance == Decimal("50")


def test_account_rejects_same_source_and_destination_on_spend(account: Account) -> None:
    with pytest.raises(ValueError, match="same"):
        account.spend(account, Decimal("20"))
    assert account.transactions == []
    assert account.balance == Decimal("50")


def test_account_accepts_zero_balance() -> None:
    acc = Account(name="Sam Sepiol", balance=Decimal("0"))
    assert acc.balance == Decimal("0")


def test_account_rejects_spending_from_zero_balance(other: Account) -> None:
    acc = Account(name="Sam Sepiol", balance=Decimal("0"))
    with pytest.raises(ValueError, match="greater"):
        acc.spend(other, Decimal("1"))
    assert acc.balance == Decimal("0")


def test_successful_spend_adds_one_transaction_to_the_account() -> None:
    acc_mrx = Account(name="Mr. X", balance=Decimal("50"))
    acc_umbrella = Account(name="Umbrella", balance=Decimal("0"))
    acc_mrx.spend(acc_umbrella, Decimal("30"))
    assert acc_mrx.transactions == [
        Transaction(source="Mr. X", destination="Umbrella", amount=Decimal("30"))
    ]
    assert acc_mrx.balance == Decimal("20")
    assert acc_umbrella.balance == Decimal("30")


def test_failed_spend_adds_nothing_to_the_accounts_transactions() -> None:
    acc_leon = Account(name="Leons S. Kennedy", balance=Decimal("30"))
    acc_rcity = Account(name="Racoon City", balance=Decimal("22"))
    with pytest.raises(ValueError, match="greater"):
        acc_leon.spend(acc_rcity, Decimal("50"))
    assert acc_leon.transactions == []
    assert acc_leon.balance == Decimal("30")
    assert acc_rcity.balance == Decimal("22")


def test_spend_succeeds_when_account_names_are_the_same() -> None:
    acc_leon = Account(name="Leons S. Kennedy", balance=Decimal("30"))
    acc_leon_clone = Account(name="Leons S. Kennedy", balance=Decimal("22"))

    acc_leon.spend(acc_leon_clone, Decimal("10"))
    assert acc_leon.transactions == [
        Transaction(acc_leon.name, acc_leon_clone.name, Decimal("10"))
    ]
    assert acc_leon.balance == Decimal("20")
    assert acc_leon_clone.balance == Decimal("32")
