#!/usr/bin/env python3

import string
from integrations import lib

# This is a simulation of ObjectMap per integration backend.

CurrencyObjectMap = lib.Datastore(
    name="Currency",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)

LocationObjectMap = lib.Datastore(
    name="Location",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)

DepartmentObjectMap = lib.Datastore(
    name="Department",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)

AccountCodeObjectMap = lib.Datastore(
    name="Account Code",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)

AccountObjectMap = lib.Datastore(
    name="Chart of Accounts",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)

VendorObjectMap = lib.Datastore(
    name="Vendor",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)

VendorBillObjectMap = lib.Datastore(
    name="Bill",
    fields=(
        "local_id",
        "remote_id",
    ),
    pk="local_id",
    keyspace=string.digits,
)
