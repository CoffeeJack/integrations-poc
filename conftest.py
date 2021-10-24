#!/usr/bin/env python3

import string
import random
import pytest
from . import database
from . import entities


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


@pytest.fixture
def random_id():
    return random.randint(1, 999)


@pytest.fixture
def random_string(length=10):
    letters = string.ascii_lowercase
    out = "".join(random.choice(letters) for i in range(length))
    return out.title()


# Fixtures for read-only entities need to deterministic since
# we'll need to match them with the remote system


@pytest.fixture
def currency(random_id):
    codes = ["CAD", "USD", "GBP"]
    return entities.Currency(
        id=random_id,
        name=random.choice(codes),
        rate=random.random(),
    )


@pytest.fixture
def location(currency, random_id, random_string):
    names = ["Vancouver", "Toronto"]
    return entities.Location(
        id=random_id,
        name=random.choice(names),
        localCurrency=currency,
    )


@pytest.fixture
def department(location, random_id, random_string):
    names = ["Marketing", "Finance", "Engineering"]
    return entities.Department(
        id=random_id,
        name=random.choice(names),
        branch=location,
    )


@pytest.fixture
def account_code(random_id, random_string):
    codes = ["1001", "2002", "3003"]
    return entities.AccountCode(
        id=random_id,
        code=random.choice(codes),
        description=random_string,
    )


@pytest.fixture
def account(random_id, account_code, department):
    return entities.Account(
        id=random_id,
        account_code=account_code,
        department=department,
    )


@pytest.fixture
def vendor(random_id, random_string, currency, location):
    return entities.Vendor(
        id=random_id,
        name=random_string,
        currency=currency,
        location=location,
    )


@pytest.fixture
def bill(random_id, random_string, vendor, account, currency):
    items = []
    for i in range(random.randint(1, 3)):
        items.append(
            entities.Item(
                id=random_id + i,
                account=account,
                description=random_string,
                quantity=random.randint(1, 5),
                unit_cost=10,
                currency=currency,
            )
        )

    return entities.Bill(
        id=random_id,
        invoice_number=f"INV{random_id}",
        vendor=vendor,
        currency=currency,
        items=items,
    )
