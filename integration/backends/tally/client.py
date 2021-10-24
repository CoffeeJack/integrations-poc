#!/usr/bin/env python3
import typing
from integration import lib
from integration.backends.tally import server
from integration.backends.tally import mapping


class Client(lib.Client):
    def send(self, body) -> lib.Response:
        status, _body = server.handle_request(
            method="POST",
            route=self.endpoint,
            body=body,
        )
        response = lib.Response(status=status, body=_body)
        return response

    def retrieve(self, key) -> lib.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/{key}"
        )
        response = lib.Response(status=status, body=body)
        return response

    def search(self, key: str, value: str) -> lib.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/?{key}={value}"
        )
        response = lib.Response(status=status, body=body)
        return response


def generate_client(entity_class: typing.Type[lib.SyncEntity]):
    return Client(
        endpoint=mapping.entity_endpoint[entity_class],
    )


def sync(entity: lib.SyncEntity, force=False):
    """
    Q: What does it mean for an object to be synced?
    A: If entities' ObjectMapStore contains a mapping of local_id to remote_id,
       it's considered as synced.
    """

    entity_class = type(entity)
    object_map = mapping.entity_datastore[entity_class]

    if entity.remote_id is not None:
        # There must be an objectmap for this. If not, something is fucky.

        if not force:
            # Entity is already synced. Nothing to do
            return
        else:
            object_map.remove(entity.local_id)
            return sync(entity)

    remote_client = generate_client(entity_class)

    # Special handling for readonly entities. We can't just push them to the
    # remote system. We need to lookup object in the remote system and store
    # the remote_id in the ObjectMap store.
    if entity_class in mapping.readonly_entity_lookup:
        lookup_key = mapping.readonly_entity_lookup[entity_class]
        response = remote_client.search(
            key=lookup_key, value=getattr(entity, lookup_key)
        )
        remote_id = response.body["id"]
    else:
        response = remote_client.send(entity.serialize())
        remote_id = response.body

    local_id = entity.local_id
    object_map.save({"local_id": local_id, "remote_id": remote_id})
