#!/usr/bin/env python3

import random
from . import generate_client, sync
from . import entities
from . import database
from . import server


class TestClient:
    def test_can_send(self, locations_datastore):
        _client = generate_client(entity_class=entities.Vendor)
        response = _client.send(
            {
                "name": "Staples",
                "location_id": random.choice(locations_datastore),
            }
        )
        assert response.status == 200, response.body
        assert response.body  # Body is the key of new resource

    def test_can_retrieve(self, locations_datastore):
        _location_key = locations_datastore[1]
        _client = generate_client(entity_class=entities.Location)
        response = _client.retrieve(_location_key)
        assert response.status == 200
        assert isinstance(response.body, dict)
        assert response.body["id"] == _location_key

    def test_can_search(self, locations_datastore):
        _client = generate_client(entity_class=entities.Location)
        response = _client.search(key="name", value="Toronto")
        assert response.status == 200
        assert isinstance(response.body, dict)
        assert response.body["name"] == "Toronto"


class TestSync:
    def test_can_sync_readonly_entities(self, currencies_datastore):
        # Check object map is empty
        assert database.CurrencyObjectMap.retrieve() == []

        # Name is intentially made different from name stored in the remote system
        currency = entities.Currency(
            local_id=1,
            remote_id=None,
            name="Canada's Dollar",
            iso_code="CAD",
        )

        result = sync(currency)

        # Check that object map has new mapping
        assert len(database.CurrencyObjectMap.retrieve()) == 1

        cad_key = currencies_datastore[0]  # CAD is the first entry in fixtures
        currency_objectmap = database.CurrencyObjectMap.retrieve(currency.local_id)
        assert currency_objectmap
        assert currency_objectmap["local_id"] == currency.local_id
        assert currency_objectmap["remote_id"] == cad_key

    def test_can_sync_entities(self, locations_datastore):
        # Ensure object map is empty and object does not exist in the remote
        # system.
        assert database.VendorObjectMap.retrieve() == []
        assert server.VendorStore.retrieve() == []

        # This location needs to exist in the remote system. To ensure that, we
        # are relying on locations_datastore. For syncing an entity, its
        # dependencies must already be sync.
        location = entities.Location(
            local_id=1, remote_id=locations_datastore[0], name="Vancouver"
        )

        vendor = entities.Vendor(
            local_id=1, remote_id=None, name="Juice Bar", location=location
        )

        result = sync(vendor)

        assert len(database.VendorObjectMap.retrieve()) == 1
        assert len(server.VendorStore.retrieve()) == 1
        assert server.VendorStore.retrieve()[0]["name"] == "Juice Bar"

        local_vendor = database.VendorObjectMap.retrieve()[0]
        remote_vendor = server.VendorStore.retrieve()[0]

        assert local_vendor["remote_id"] == remote_vendor["id"]
