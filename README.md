# Integrations PoC

This is proof-of-concept project that demonstrates usage of a directed graph to
resolve dependencies and sync with a remote systems.

For this demo, `tally` is an accounting system we need to integrate with. It
supports the following objects:

Currency (Read only)

| Attribute | Type   |
| --------- | ------ |
| id        | int    |
| name      | string |
| iso_code  | string |

Location (Read only)

| Attribute | Type   |
| --------- | ------ |
| id        | int    |
| name      | string |

Department (Read only)

| Attribute | Type   |
| --------- | ------ |
| id        | int    |
| name      | string |

Chart of Accounts (Read only)

| Attribute | Type   |
| --------- | ------ |
| id        | int    |
| number    | string |
| name      | string |

Vendor

| Attribute | Type     |
| --------- | -------- |
| id        | int      |
| name      | string   |
| location  | Location |

Vendor Bill

| Attribute | Type             |
| --------- | ---------------- |
| id        | int              |
| account   | Chart of Account |
| vendor    | Vendor           |
| currency  | Currency         |
| location  | Location         |
| items     | [Item]           |

Item (Only synced via Vendor Bill)

| Attribute   | Type   |
| ----------- | ------ |
| description | string |
| quantity    | int    |
| rate        | int    |
| total       | int    |

# Usage

```python
from integration.services import sync

result = sync(entity=local_entity, backend='tally')
```

# Demo

**Demo 1**

Syncing a readonly entity.

Currency is a readonly entity such that remote system does not allow creating
new instances of it. The only way it can be synced is by creating a local
instance of it with key/value matching the criteria that will be used to look
it up in the remote system. In Currency's case, the look up key is "iso_code"
as defined in backend's mapping definition.

**Demo 2**

Syncing an entity with simple depencencies.

In this example, we'll sync a vendor which has location as a dependency.
However, Location is a readonly entity. So, we'll need to ensure it's synced
before syncing Vendor.

Notice that although currency is an attribute of local location and vendor,
it's not synced because vendor and location in the remote system don't have it.

```sh
(integration) ➜  integration git:(main) ✗ SLOWMO=1 python demo.py
Running Demo 1:
SyncResult(status=<SyncStatus.CREATED: 0>, message="Sync created for '<Currency local_id=1 remote_id=None>'")
SyncResult(status=<SyncStatus.IN_PROGRESS: 1>, message="Sync in progress for '<Currency local_id=1 remote_id=None>'")
SyncResult(status=<SyncStatus.COMPLETED: 2>, message='Entity synced successfully.')
Result = <Currency local_id=1 remote_id=y961l2>
Running Demo 2:
SyncResult(status=<SyncStatus.CREATED: 0>, message="Sync created for '<Location local_id=1 remote_id=None>'")
SyncResult(status=<SyncStatus.IN_PROGRESS: 1>, message="Sync in progress for '<Location local_id=1 remote_id=None>'")
SyncResult(status=<SyncStatus.COMPLETED: 2>, message='Entity synced successfully.')
SyncResult(status=<SyncStatus.CREATED: 0>, message="Sync created for '<Vendor local_id=1 remote_id=None>'")
SyncResult(status=<SyncStatus.IN_PROGRESS: 1>, message="Sync in progress for '<Vendor local_id=1 remote_id=None>'")
SyncResult(status=<SyncStatus.COMPLETED: 2>, message='Entity synced successfully.')
Result = <Vendor local_id=1 remote_id=x8huc8>
```

# Testing

You'll need `pytest` to be able to run tests. To setup testing environment:

```sh
➜  integration git:(main) ✗ pipenv install --dev && pipenv shell
(integration) ➜  integration git:(main) ✗ pytest
```
