import typing
from integration import lib
from integration import entities as local_entities
from integration.backends.tally import entities as remote_entities
from integration.backends.tally import database


mapping = lib.Mapping(
    local_remote_entity={
        local_entities.Currency: remote_entities.Currency,
        local_entities.Location: remote_entities.Location,
        local_entities.Department: remote_entities.Department,
        local_entities.Account: remote_entities.ChartOfAccounts,
        local_entities.Vendor: remote_entities.Vendor,
        local_entities.Bill: remote_entities.VendorBill,
    },
    readonly_entity_lookup={
        remote_entities.Currency: "iso_code",
        remote_entities.Location: "name",
        remote_entities.Department: "name",
        remote_entities.ChartOfAccounts: "number",
    },
    entity_endpoint={
        remote_entities.Currency: "/currencies",
        remote_entities.Location: "/locations",
        remote_entities.Department: "/departments",
        remote_entities.ChartOfAccounts: "/coa",
        remote_entities.Vendor: "/vendors",
        remote_entities.VendorBill: "/vendorbills",
    },
    entity_datastore={
        remote_entities.Currency: database.CurrencyObjectMap,
        remote_entities.Location: database.LocationObjectMap,
        remote_entities.Department: database.DepartmentObjectMap,
        remote_entities.ChartOfAccounts: database.AccountCodeObjectMap,
        remote_entities.Vendor: database.VendorObjectMap,
        remote_entities.VendorBill: database.VendorBillObjectMap,
    },
)


def generate_client(entity_class: typing.Type[lib.SyncEntity]):
    # TODO(nav): Remove local import
    from integration.backends.tally.client import Client

    return Client(
        endpoint=mapping.entity_endpoint[entity_class],
    )


def sync(entity: lib.SyncEntity, force=False) -> lib.SyncResult:
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
            return lib.SyncResult(
                status=lib.SyncStatus.COMPLETED,
                message="Object is already synced.",
            )
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
        if response.status != 200:
            return lib.SyncResult(status=lib.SyncStatus.ERROR, message=response.body)
        remote_id = response.body["id"]
    else:
        response = remote_client.send(entity.serialize())
        if response.status != 200:
            return lib.SyncResult(status=lib.SyncStatus.ERROR, message=response.body)
        remote_id = response.body

    local_id = entity.local_id

    object_map.save({"local_id": local_id, "remote_id": remote_id})
    return lib.SyncResult(
        status=lib.SyncStatus.COMPLETED,
        message="Entity synced successfully.",
    )
