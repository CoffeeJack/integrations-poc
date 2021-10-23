#!/usr/bin/env python3

import typing
from integrations import entities

DepartmentStore: typing.List[entities.SyncEntity] = []
LocationStore: typing.List[entities.SyncEntity] = []
CurrencyStore: typing.List[entities.SyncEntity] = []
AccountStore: typing.List[entities.SyncEntity] = []
VendorStore: typing.List[entities.SyncEntity] = []
BillStore: typing.List[entities.SyncEntity] = []


entity_datastore_mapping = {
    entities.Department: DepartmentStore,
    entities.Location: LocationStore,
    entities.Currency: CurrencyStore,
    entities.Account: AccountStore,
    entities.Vendor: VendorStore,
    entities.Bill: BillStore,
}


class DataStoreException(Exception):
    pass


def _get_store_for_entity_class(entity_class: typing.Type[entities.SyncEntity]):
    try:
        return entity_datastore_mapping[entity_class]
    except KeyError:
        raise DataStoreException(
            f"Could not find datastore for entity '{entity_class.__name__}'"
        )


def retrieve(entity_class: typing.Type[entities.SyncEntity], id: int):
    store = _get_store_for_entity_class(entity_class)

    try:
        return store[id - 1]
    except IndexError:
        raise DataStoreException(
            f"Could not find entity '{entity_class.__name__}={id}'"
        )


def save(entity: entities.SyncEntity):
    store = _get_store_for_entity_class(type(entity))
    store[entity.local_id - 1] = entity
