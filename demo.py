#!/usr/bin/env python3

from integration.backends.tally import server
from integration.backends.tally import entities as remote_entities
from integration import entities
from integration import services


"""
Demo 1: Syncing a readonly entity.

Currency is a readonly entity such that remote system does not allow creating
new instances of it. The only way it can be synced is by creating a local
instance of it with key/value matching the criteria that will be used to look
it up in the remote system. In Currency's case, the look up key is "iso_code"
as defined in backend's mapping definition.
"""

print("Running Demo 1:")

# Prepare remote system
remote_id = server.CurrencyStore.save(
    {
        "name": "Canadian Dollar",
        "iso_code": "CAD",
    }
)

# Prepare local entity
currency = entities.Currency(id=1, name="CAD", rate=1)

result = services.sync(entity=currency, backend="tally")
while result:
    try:
        res = next(result)
    except StopIteration:
        break
    print(res)

# Inspect object map that it contains remote id
remote_entity = remote_entities.Currency.from_local(currency)
print(f"Result = {remote_entity}")


"""
Demo 2: Syncing an entity with simple depencencies.

In this example, we'll sync a vendor which has location as a dependency.
However, Location is a readonly entity. So, we'll need to ensure it's synced
before syncing Vendor.

Notice that although currency is an attribute of local location and vendor,
it's not synced because vendor and location in the remote system don't have it.
"""

print("Running Demo 2:")


# Prepare remote system
remote_id = server.LocationStore.save(
    {
        "name": "Vancouver",
    }
)

location = entities.Location(
    id=1, name="Vancouver", localCurrency=currency
)  # Currency is from demo 1
vendor = entities.Vendor(id=1, name="Staples", currency=currency, location=location)

result = services.sync(entity=vendor, backend="tally")
while result:
    try:
        res = next(result)
    except StopIteration:
        break
    print(res)

remote_entity = remote_entities.Vendor.from_local(vendor)
print(f"Result = {remote_entity}")
