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

    def retrieve(self, id) -> client.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/{id}"
        )
        response = client.Response(status=status, body=body)
        return response


entity_endpoint_mapping: typing.Dict[typing.Type[entities.SyncEntity], str] = {
    entities.Currency: "/currencies",
    entities.Location: "/locations",
    entities.Department: "/departments",
    entities.ChartOfAccounts: "/coa",
    entities.Vendor: "/vendors",
    entities.VendorBill: "/vendorbills",
}

readonly_entities = {
    entities.Currency,
    entities.Location,
    entities.Department,
    entities.ChartOfAccounts,
}


def generate_client(entity_class: typing.Type[entities.SyncEntity]):
    return Client(
        endpoint=entity_endpoint_mapping[entity_class],
    )


def sync(entity: entities.SyncEntity, force=False):
    entity_class = type(entity)
    object_map = database.entity_datastore_mapping[entity_class]

    if entity.id is not None:
        if not force:
            # Entity is already synced. Nothing to do
            return
        else:
            object_map.remove(entity.id)
            return sync(entity)

    if entity_class in readonly_entities:
        remote_client = generate_client(entity_class)
        response = remote_client.retrieve()


# def sync(entity: entities.SyncEntity):

#     entity_class = type(entity)
#     try:
#         entity = database.retrieve(entity_class, entity.local_id)
#     except database.DataStoreException:
#         # Don't sync entities that don't have a datastore. For example,
#         # bill item shouldn't be synced without a bill.
#         return

#     if entity.remote_id is not None:
#         # This entity is already synced.
#         return

#     remote_client = generate_client(entity_class)
#     response = remote_client.send(entity.serialize())

#     entity = entity_class.deserialize(response.body)
#     database.save(entity)
