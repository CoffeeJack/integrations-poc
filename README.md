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

| Attribute | Type   |
| --------- | ------ |
| id        | int    |
| name      | string |

Vendor Bill

| Attribute  | Type             |
| ---------- | ---------------- |
| id         | int              |
| invoice    | string           |
| account    | Chart of Account |
| vendor     | Vendor           |
| currency   | Currency         |
| location   | Location         |
| department | Department       |
| items      | [Item]           |

Item

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

# Components

There are three main components:

- Entities: These refer to objects that can be synced with a remote system.
- Graph: Represented as adjacency list this module contains function to generate
  graph and traverse it using depth first search.
- Remote: This is essential a stub simulating the remote system.
