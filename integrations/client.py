#!/usr/bin/env python3
import typing
import dataclasses
from integrations import entities
from integrations import remote
from integrations import database


@dataclasses.dataclass(frozen=True)
class Response:
    status: int
    body: dict


class Client:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def send(self, body) -> Response:
        status, _body = remote.handle_request(
            method="POST",
            route=self.endpoint,
            body=body,
        )
        response = Response(status=status, body=_body)
        return response

    def retrieve(self, id) -> Response:
        status, body = remote.handle_request(
            method="GET", route=f"{self.endpoint}/{id}"
        )
        response = Response(status=status, body=body)
        return response


entity_endpoint_mapping: typing.Dict[typing.Type[entities.SyncEntity], str] = {
    entities.Department: "/departments",
    entities.Location: "/locations",
    entities.Currency: "/currencies",
    entities.Account: "/accounts",
    entities.Vendor: "/vendors",
    entities.Bill: "/bills",
}


def generate_client(entity_class: typing.Type[entities.SyncEntity]):
    return Client(
        endpoint=entity_endpoint_mapping[entity_class],
    )


def sync(entity: entities.SyncEntity):

    entity_class = type(entity)
    try:
        entity = database.retrieve(entity_class, entity.local_id)
    except database.DataStoreException:
        # Don't sync entities that don't have a datastore. For example,
        # bill item shouldn't be synced without a bill.
        return

    if entity.remote_id is not None:
        # This entity is already synced.
        return

    remote_client = generate_client(entity_class)
    response = remote_client.send(entity.serialize())

    entity = entity_class.deserialize(response.body)
    database.save(entity)
