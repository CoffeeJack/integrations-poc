#!/usr/bin/env python3

import pytest
from . import server


@pytest.fixture(autouse=True)
def reset_datastores():
    server.CurrencyStore.reset()
    server.LocationStore.reset()
    server.DepartmentStore.reset()
    server.ChartOfAccountsStore.reset()
    server.VendorStore.reset()
    server.VendorBillStore.reset()
