# Integrations PoC

This is proof-of-concept project that demonstrates usage of a directed graph to
resolve dependencies and sync with a remote systems.

## Definitions

- Local system: System that needs to sync it's object.
- Remote system: System we need to sync objects with.
- Sync: Ability to maintain reference to object in the remote system.

## Problem Statement

> Given an object that exists in local system, we need the ability to sync it
> with a remote system along with its dependencies.

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

## Structure

Relevant code files:

```sh
.
├── demo.py
└── integration
    ├── __init__.py
    ├── backends
    │   ├── __init__.py             - Allows fetching the given backend.
    │   └── tally
    │       ├── __init__.py
    │       ├── client.py           - Frontend to the remote system.
    │       ├── database.py         - Storage of local -> remote references.
    │       ├── entities.py         - Acceptable entities by the remote system.
    │       └── server.py           - Fake implementation of the remote system.
    ├── conftest.py
    ├── database.py                 - Database that stores local entities.
    ├── entities.py                 - Entities as defined in the local system.
    ├── graph.py                    - Generates and traverses dependency graph
    ├── lib.py                      - Shared components
    └── services.py                 - Entrypoint for the integrations.
```

## Usage

```python
from integration.services import sync

result = sync(entity=local_entity, backend='tally')
```

## Demo

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

## Testing

You'll need `pytest` to be able to run tests. To setup testing environment:

```sh
➜  integration git:(main) ✗ pipenv install --dev && pipenv shell
(integration) ➜  integration git:(main) ✗ pytest
```
