#!/usr/bin/env python3
import typing
import dataclasses
from integrations.backends.entities import SyncEntity


@dataclasses.dataclass(eq=False, frozen=True)
class Currency(SyncEntity):
    name: str
    iso_code: str


@dataclasses.dataclass(eq=False, frozen=True)
class Location(SyncEntity):
    name: str


@dataclasses.dataclass(eq=False, frozen=True)
class Department(SyncEntity):
    name: str


@dataclasses.dataclass(eq=False, frozen=True)
class ChartOfAccounts(SyncEntity):
    number: str
    name: str


@dataclasses.dataclass(eq=False, frozen=True)
class Vendor(SyncEntity):
    name: str
    location: Location


@dataclasses.dataclass(eq=False, frozen=True)
class Item(SyncEntity):
    description: str
    quantity: int
    rate: int
    total: int
    currency: Currency

    def serialize(self):
        ser = super().serialize()
        ser.update({"currency": self.currency.serialize()})
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class VendorBill(SyncEntity):
    invoice: str
    account: ChartOfAccounts
    vendor: Vendor
    currency: Currency
    location: Location
    department: Department
    items: typing.List[Item]

    def serialize(self):
        ser = super().serialize()
        ser.update(
            {
                "account": self.account.serialize(),
                "vendor": self.vendor.serialize(),
                "currency": self.currency.serialize(),
                "location": self.location.serialize(),
                "department": self.department.serialize(),
                "items": [item.serialize() for item in self.items],
            }
        )
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class BillCollection(SyncEntity):
    """Only used as a container of bills. Does not refer to an entity in the
    remote system.
    """

    bills: typing.List[VendorBill]

    def serialize(self):
        return {"bills": [bill.serialize() for bill in self.bills]}