#!/usr/bin/env python3

import pytest
import dataclasses
from . import entities


@pytest.fixture
def House():
    @dataclasses.dataclass(eq=False, frozen=True)
    class House(entities.SyncEntity):
        size: int
        beds: int
        baths: int

        def serialize(self):
            return dataclasses.asdict(self)

    return House


@pytest.fixture
def house(House):
    return House(id=1, size=2800, beds=5, baths=3)


class TestSyncEntity:
    def test_can_create_entity(self, House):
        house = House(id=None, size=4000, beds=3, baths=3)
        assert house.id is None

    def test_equality(self, House):
        house1 = House(id=1, size=1000, beds=2, baths=2)
        house2 = House(id=1, size=2000, beds=4, baths=2)
        assert house1 == house2

    def test_can_serialize(self, house):
        data = house.serialize()
        assert isinstance(data, dict)
        assert data["id"] == house.id
        assert data["size"] == house.size

    def test_can_deserialize(self, House):
        house = House.deserialize({"id": 999, "size": 1000, "beds": 2, "baths": 1})
        assert house.id == 999