#!/usr/bin/env python3

import string
from integrations import lib
from integrations import entities

# This is a simulation of local database.

CurrencyStore = lib.Datastore(
    name="Currency",
    fields=(
        "id",
        "name",
        "rate",
    ),
    keyspace=string.digits,
)

LocationStore = lib.Datastore(
    name="Location",
    fields=(
        "id",
        "name",
        "localCurrency_id",
    ),
    keyspace=string.digits,
)

DepartmentStore = lib.Datastore(
    name="Department",
    fields=(
        "id",
        "name",
        "branch_id",
    ),
    keyspace=string.digits,
)

AccountCodeStore = lib.Datastore(
    name="Account Code",
    fields=(
        "id",
        "code",
        "description",
    ),
    keyspace=string.digits,
)

AccountStore = lib.Datastore(
    name="Chart of Accounts",
    fields=(
        "id",
        "number",
        "name",
    ),
    keyspace=string.digits,
)

VendorStore = lib.Datastore(
    name="Vendor",
    fields=(
        "id",
        "name",
        "currency_id",
    ),
    keyspace=string.digits,
)

ItemStore = lib.Datastore(
    name="Item",
    fields=(
        "id",
        "account_id",
        "description",
        "quantity",
        "unit_cost",
    ),
    keyspace=string.digits,
)

BillStore = lib.Datastore(
    name="Bill",
    fields=(
        "id",
        "invoice_number",
        "vendor_id",
        "currency_id",
        "items",
    ),
    keyspace=string.digits,
)


entity_datastore_mapping = {
    entities.Currency: CurrencyStore,
    entities.Location: LocationStore,
    entities.Department: DepartmentStore,
    entities.AccountCode: AccountCodeStore,
    entities.Account: AccountStore,
    entities.Vendor: VendorStore,
    entities.Item: ItemStore,
    entities.Bill: BillStore,
}
