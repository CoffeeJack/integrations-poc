#!/usr/bin/env python3


import pytest
from . import database


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
