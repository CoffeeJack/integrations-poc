#!/usr/bin/env python3

import string
import random
import pytest
from integration import database
from integration import entities


def random_id():
    return random.randint(1, 999)


def random_string(length=10):
    letters = string.ascii_lowercase
    out = "".join(random.choice(letters) for i in range(length))
    return out.title()


@pytest.fixture(autouse=True)
def reset_datastores():
    database.CurrencyStore.reset()
    database.LocationStore.reset()
    database.DepartmentStore.reset()
    database.AccountCodeStore.reset()
    database.AccountStore.reset()
    database.VendorStore.reset()
    database.ItemStore.reset()
    database.BillStore.reset()


# Fixtures for read-only entities need to be deterministic because
# we'll need to match them with the remote system.


@pytest.fixture
def currency():
    codes = ["CAD", "USD", "GBP"]
    return entities.Currency(
        id=random_id(),
        name=random.choice(codes),
        rate=random.random(),
    )


@pytest.fixture
def location(currency):
    names = ["Vancouver", "Toronto"]
    return entities.Location(
        id=random_id(),
        name=random.choice(names),
        localCurrency=currency,
    )


@pytest.fixture
def department(location):
    names = ["Marketing", "Finance", "Engineering"]
    return entities.Department(
        id=random_id(),
        name=random.choice(names),
        branch=location,
    )


@pytest.fixture
def account_code():
    codes = ["1001", "2002", "3003"]
    return entities.AccountCode(
        id=random_id(),
        code=random.choice(codes),
        description=random_string(),
    )


@pytest.fixture
def account(account_code, department):
    return entities.Account(
        id=random_id(),
        account_code=account_code,
        department=department,
    )


@pytest.fixture
def vendor(currency, location):
    return entities.Vendor(
        id=random_id(),
        name=random_string(),
        currency=currency,
        location=location,
    )


@pytest.fixture
def bill(vendor, account, currency):
    bill_id = random_id()
    items = []
    for i in range(random.randint(1, 3)):
        items.append(
            entities.Item(
                id=bill_id + i,
                account=account,
                description=random_string(),
                quantity=random.randint(1, 5),
                unit_cost=10,
                currency=currency,
            )
        )

    return entities.Bill(
        id=bill_id,
        invoice_number=f"INV{random_id()}",
        vendor=vendor,
        currency=currency,
        items=items,
    )
