#!/usr/bin/env python3
import os
import time
import typing
from integration import lib
from integration import graph
from integration.backends import get_backend


def sync(entity, backend: str) -> typing.Iterator[lib.SyncResult]:
    """Sync the given entity with remote backend.

    Args:
        entity: A fully deserialized instance of local entity.
        backend: Name of the backend to be used for syncing.

    Returns:
        An instance of SyncResult.

    Raises:
        BackendError: Given backend does not exist.
    """

    is_slow_mo = int(os.environ.get("SLOWMO", 0))

    # Lookup backend to used for syncing.
    _backend = get_backend(backend)
    mapping = _backend.mapping

    # Find and instantiate corresponding remote entity for the given local
    # entity. The process will also instantiate any dependent entities.
    remote_entity_class = mapping.local_remote_entity[type(entity)]
    remote_entity = remote_entity_class.from_local(entity)

    # Generate a dependency graph that will be used to put entities in the
    # order in which they should be synced.
    graph_root = graph.generate_graph(remote_entity)

    # Resolve dependencies for the given graph root. It'll also remove
    # duplicates and only include shared dependencies once while
    # retaining the order.
    remote_entities_to_be_synced = graph.resolve_dependencies(graph_root)

    for remote_entity in remote_entities_to_be_synced:
        yield lib.SyncResult(
            status=lib.SyncStatus.CREATED,
            message=f"Sync created for '{remote_entity}'",
        )
        if is_slow_mo:
            time.sleep(2)

        yield lib.SyncResult(
            status=lib.SyncStatus.IN_PROGRESS,
            message=f"Sync in progress for '{remote_entity}'",
        )
        if is_slow_mo:
            time.sleep(2)

        result = _backend.sync(remote_entity)
        yield result
        if is_slow_mo:
            time.sleep(3)
