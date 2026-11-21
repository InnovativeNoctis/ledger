from decimal import Decimal

import pytest

from ledger.account import Account


@pytest.fixture
def account():
    return Account(name="Sam Sepiol", balance=Decimal("50"))


def test_account_keeps_its_name(account):
    assert account.name == "Sam Sepiol"


def test_account_rejects_whitespaces_only_name():
    with pytest.raises(ValueError):
        Account(name="       ", balance=Decimal("50"))


def test_account_keeps_its_balance(account):
    assert account.balance == Decimal("50")


def test_account_rejects_empty_name():
    with pytest.raises(ValueError):
        Account(name="", balance=Decimal("50"))


def test_account_rejects_negative_balance():
    with pytest.raises(ValueError, match="negative"):
        Account(name="Sam Sepiol", balance=Decimal("-5"))


def test_account_accepts_spending_with_positive_number(account):
    account.spend(Decimal("30"))
    assert account.balance == Decimal("20")


def test_account_accepts_spending_equal_to_balance(account):
    account.spend(Decimal("50"))
    assert account.balance == Decimal("0")


def test_account_rejects_spending_with_negative_number(account):
    with pytest.raises(ValueError, match="negative"):
        account.spend(Decimal("-30"))
    assert account.balance == Decimal("50")


def test_account_rejects_spending_with_zero_number(account):
    with pytest.raises(ValueError, match="zero"):
        account.spend(Decimal("0"))
    assert account.balance == Decimal("50")


def test_account_rejects_spending_more_than_balance(account):
    with pytest.raises(ValueError, match="greater"):
        account.spend(Decimal("60"))
    assert account.balance == Decimal("50")


def test_account_accepts_zero_balance():
    acc = Account(name="Sam Sepiol", balance=Decimal("0"))
    assert acc.balance == Decimal("0")


def test_account_rejects_spending_from_zero_balance():
    acc = Account(name="Sam Sepiol", balance=Decimal("0"))
    with pytest.raises(ValueError, match="greater"):
        acc.spend(Decimal("1"))
    assert acc.balance == Decimal("0")
