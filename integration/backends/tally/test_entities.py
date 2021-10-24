#!/usr/bin/env python3

from integration import graph
from integration.backends.tally import entities


class TestEntity:
    def test_can_instantiate_from_local(self, bill):
        vendor_bill = entities.VendorBill.from_local(bill)
        assert vendor_bill

        assert vendor_bill.local_id == bill.id
        assert vendor_bill.remote_id is None

    def test_can_serialize(self, bill):
        vendor_bill = entities.VendorBill.from_local(bill)

        serialized = vendor_bill.serialize()
        assert serialized
        assert serialized["local_id"] == bill.id
        assert serialized["remote_id"] is None


class TestGraph:
    def test_can_generate_graph(self, bill):
        sync_entity = entities.VendorBill.from_local(bill)
        node = graph.generate_graph(sync_entity)
        assert node
        assert node.deps
