#!/usr/bin/env python3

import pytest
from . import server


class TestAPI:
    def test_can_create_record(self, locations_datastore):
        status, body = server.handle_request(
            "POST",
            "/vendors",
            {"name": "Corner Flower Shop", "location_id": locations_datastore[0]},
        )
        assert status == 200, body
        assert body

    def test_can_get_record(self, currencies_datastore):
        currency_id = currencies_datastore[0]
        status, body = server.handle_request("GET", f"/currencies/{currency_id}")
        assert status == 200
        assert body["id"] == currency_id

    @pytest.mark.parametrize(
        "key_value_pair", [("name", "Canadian Dollar"), ("iso_code", "GBP")]
    )
    def test_can_search_record(self, key_value_pair, currencies_datastore):
        key, value = key_value_pair
        status, body = server.handle_request("GET", f"/currencies/?{key}={value}")
        assert status == 200
        assert body[key] == value, body
