#!/usr/bin/env python3

import pytest
from . import server


@pytest.fixture
def currencies():
    _currencies = [
        {"name": "Canadian Dollar", "iso_code": "CAD"},
        {"name": "US Dollar", "iso_code": "USD"},
        {"name": "British Pound sterling", "iso_code": "GBP"},
    ]
    keys = []
    for _c in _currencies:
        keys.append(server.CurrencyStore.save(_c))
    return keys


class TestAPI:
    def test_can_create_record(self):
        status, body = server.handle_request("POST", "/vendors", {"name": "Vancouver"})
        assert status == 200
        assert body

    def test_can_get_record(self, currencies):
        currency_id = currencies[0]
        status, body = server.handle_request("GET", f"/currencies/{currency_id}")
        assert status == 200
        assert body["id"] == currency_id

    @pytest.mark.parametrize(
        "key_value_pair", [("name", "Canadian Dollar"), ("iso_code", "GBP")]
    )
    def test_can_search_record(self, key_value_pair, currencies):
        key, value = key_value_pair
        status, body = server.handle_request("GET", f"/currencies/?{key}={value}")
        assert status == 200
        assert body[key] == value, body
