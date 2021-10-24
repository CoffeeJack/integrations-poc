#!/usr/bin/env python3
import typing
from integrations.backends import client
from integrations.backends.tally import server
from integrations.backends.tally import entities
from integrations.backends.tally import database


class Client(client.Client):
    def send(self, body) -> client.Response:
        status, _body = server.handle_request(
            method="POST",
            route=self.endpoint,
            body=body,
        )
        response = client.Response(status=status, body=_body)
        return response

    def retrieve(self, key) -> client.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/{key}"
        )
        response = client.Response(status=status, body=body)
        return response

    def search(self, key: str, value: str) -> client.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/?{key}={value}"
        )
        response = client.Response(status=status, body=body)
        return response


# Mapping of entity class and remote endpoint
entity_endpoint_mapping: typing.Dict[typing.Type[entities.SyncEntity], str] = {
    entities.Currency: "/currencies",
    entities.Location: "/locations",
    entities.Department: "/departments",
    entities.ChartOfAccounts: "/coa",
    entities.Vendor: "/vendors",
    entities.VendorBill: "/vendorbills",
}

# Mapping of entity class and key to use when looking up remote instance
readonly_entities = {
    entities.Currency: "iso_code",
    entities.Location: "name",
    entities.Department: "name",
    entities.ChartOfAccounts: "number",
}


def generate_client(entity_class: typing.Type[entities.SyncEntity]):
    return Client(
        endpoint=entity_endpoint_mapping[entity_class],
    )


def sync(entity: entities.SyncEntity, force=False):
    """
    Q: What does it mean for an object to be synced?
    A: If entities' ObjectMapStore contains a mapping of local_id to remote_id,
       it's considered as synced.
    """

    entity_class = type(entity)
    object_map = database.entity_datastore_mapping[entity_class]

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
    if entity_class in readonly_entities:
        lookup_key = readonly_entities[entity_class]
        response = remote_client.search(
            key=lookup_key, value=getattr(entity, lookup_key)
        )
        remote_id = response.body["id"]
    else:
        response = remote_client.send(entity.serialize())
        remote_id = response.body

    local_id = entity.local_id
    object_map.save({"local_id": local_id, "remote_id": remote_id})
