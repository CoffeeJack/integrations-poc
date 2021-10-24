#!/usr/bin/env python3
import string
import random
from integrations import entities
from integrations import database


def _rand_string(length=10):
    letters = string.ascii_lowercase
    out = "".join(random.choice(letters) for i in range(length))
    return out.title()


def location_generator(count=1):
    entity = entities.Location
    store = database.entity_datastore_mapping[entity]

    for _ in range(count):
        entity_id = len(store) + 1
        _entity = entity(name=_rand_string(8), local_id=entity_id, remote_id=None)
        store.append(_entity)
        assert len(store) == entity_id
        yield _entity


def department_generator(count=1):
    entity = entities.Department
    store = database.entity_datastore_mapping[entity]

    for _ in range(count):
        entity_id = len(store) + 1
        _entity = entity(name=_rand_string(8), local_id=entity_id, remote_id=None)
        store.append(_entity)
        assert len(store) == entity_id
        yield _entity


def vendor_generator(currency, count=1):
    entity = entities.Vendor
    store = database.entity_datastore_mapping[entity]

    for _ in range(count):
        entity_id = len(store) + 1
        _entity = entity(
            name=_rand_string(8),
            currency=currency,
            local_id=entity_id,
            remote_id=None,
        )
        store.append(_entity)
        assert len(store) == entity_id
        yield _entity


def account_generator(locations, departments, count=1):
    entity = entities.Account
    store = database.entity_datastore_mapping[entity]

    for _ in range(count):
        entity_id = len(store) + 1
        _entity = entity(
            code=_rand_string(4),
            location=random.choice(locations),
            department=random.choice(departments),
            local_id=entity_id,
            remote_id=None,
        )
        store.append(_entity)
        assert len(store) == entity_id
        yield _entity


def billitem_generator(accounts, currency, prefix=0, count=10):
    entity = entities.BillItem

    for i in range(count):
        entity_id = i
        _entity = entity(
            account=random.choice(accounts),
            name=_rand_string(10),
            quantity=random.randint(1, 10),
            unit_cost=random.randint(10, 100),
            currency=currency,
            local_id=prefix * 10 + entity_id,  # To create unique items per bill
            remote_id=None,
        )
        yield _entity


def bill_generator(accounts, currency, vendors, count=1):
    entity = entities.Bill
    store = database.entity_datastore_mapping[entity]

    for i in range(count):
        items = list(
            billitem_generator(
                accounts,
                currency,
                prefix=i,
                count=random.randint(2, 3),
            )
        )

        entity_id = len(store) + 1
        _entity = entity(
            vendor=random.choice(vendors),
            invoice_number=f"INV{random.randint(1000, 9999)}",
            items=items,
            local_id=entity_id,
            remote_id=None,
        )
        store.append(_entity)
        assert len(store) == entity_id
        yield _entity


def billcollection_generator(count=1):
    locations = list(location_generator(count=3))
    departments = list(department_generator(count=5))

    currency = entities.Currency(code="CAD", local_id=1, remote_id=None)
    database.entity_datastore_mapping[entities.Currency].append(currency)

    vendors = list(vendor_generator(currency, count=10))
    accounts = list(account_generator(locations, departments, count=1))

    bills = list(bill_generator(accounts, currency, vendors, count=count))
    return entities.BillCollection(bills=bills, local_id=1, remote_id=None)
