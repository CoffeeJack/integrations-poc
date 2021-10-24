#!/usr/bin/env python3

import pytest
from . import server
from . import database


@pytest.fixture(autouse=True)
def reset_datastores():
    server.CurrencyStore.reset()
    server.LocationStore.reset()
    server.DepartmentStore.reset()
    server.ChartOfAccountsStore.reset()
    server.VendorStore.reset()
    server.VendorBillStore.reset()

    database.CurrencyObjectMap.reset()
    database.LocationObjectMap.reset()
    database.DepartmentObjectMap.reset()
    database.CurrencyObjectMap.reset()
    database.VendorObjectMap.reset()
    database.VendorBillObjectMap.reset()


@pytest.fixture
def currencies_datastore():
    _currencies = [
        {"name": "Canadian Dollar", "iso_code": "CAD"},
        {"name": "US Dollar", "iso_code": "USD"},
        {"name": "British Pound sterling", "iso_code": "GBP"},
    ]
    keys = []
    for c in _currencies:
        keys.append(server.CurrencyStore.save(c))
    return keys


@pytest.fixture
def locations_datastore():
    _locations = [
        {"name": "Vancouver"},
        {"name": "Toronto"},
    ]
    keys = []
    for l in _locations:
        keys.append(server.LocationStore.save(l))
    return keys
