#!/usr/bin/env python3

import pytest
import typing
import dataclasses
from integrations.backends import entities
from integrations.backends import graph


@dataclasses.dataclass(eq=False, frozen=True)
class Appliance(entities.SyncEntity):
    name: str


@dataclasses.dataclass(eq=False, frozen=True)
class Window(entities.SyncEntity):
    width: int
    height: int


@dataclasses.dataclass(eq=False, frozen=True)
class Room(entities.SyncEntity):
    name: str
    windows: typing.List[Window]
    appliance: typing.Optional[Appliance]
    fans: typing.Optional[int] = None


@dataclasses.dataclass(eq=False, frozen=True)
class House(entities.SyncEntity):
    name: str
    rooms: typing.List[Room]
    appliances: typing.List[Appliance]


@pytest.fixture
def house():
    stove = Appliance(local_id=1, remote_id=None, name="Stove")
    washer = Appliance(local_id=2, remote_id=None, name="Washer")
    window = Window(local_id=1, remote_id=None, width=2, height=4)
    laundry_room = Room(
        local_id=1,
        remote_id=None,
        name="Laundry Room",
        windows=[window],
        appliance=washer,
    )

    house = House(
        local_id=1,
        remote_id=None,
        name="A House",
        rooms=[laundry_room],
        appliances=[stove, washer],
    )

    return house


class TestGraph:
    def test_can_generate_graph(self, house):
        node = graph.generate_graph(house)

        assert node

        # House has 3 dependencies: Laundry Room, Stove, Washer
        assert len(node.deps) == 3, node.deps

        # Room has 2 dependency: Window, Washer
        assert len(node.deps[0].deps) == 2, node.deps[0].deps

        # Shared washer only exists as as one node
        house_washer = None
        for dep in node.deps:
            if dep.entity.name == "Washer":
                house_washer = dep

        laundry_washer = node.deps[0].deps[1]
        assert house_washer == laundry_washer

    def test_can_traverse_graph(self, house):
        node = graph.generate_graph(house)
        deps = graph.resolve_dependencies(node)

        assert deps
        assert len(deps) == 5

        # Order should be preserved
        washer, window, stove, room, _house = deps
        assert washer.name == "Washer"
        assert window.width == 2
        assert stove.name == "Stove"
        assert room.name == "Laundry Room"
        assert _house == house
