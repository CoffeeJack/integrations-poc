#!/usr/bin/env python3
import typing
import dataclasses

from integrations import lib
from integrations.backends.tally import database


@dataclasses.dataclass(eq=False, frozen=True)
class Currency(lib.SyncEntity):
    name: str
    iso_code: str

    @classmethod
    def from_local(cls, orm):
        return cls(
            local_id=orm.id,
            remote_id=database.CurrencyObjectMap.retrieve(orm.id),
            name=orm.name,
            iso_code=orm.name,
        )


@dataclasses.dataclass(eq=False, frozen=True)
class Location(lib.SyncEntity):
    name: str

    @classmethod
    def from_local(cls, orm):
        return cls(
            local_id=orm.id,
            remote_id=database.LocationObjectMap.retrieve(orm.id),
            name=orm.name,
        )


@dataclasses.dataclass(eq=False, frozen=True)
class Department(lib.SyncEntity):
    name: str

    @classmethod
    def from_local(cls, orm):
        return cls(
            local_id=orm.id,
            remote_id=database.DepartmentObjectMap.retrieve(orm.id),
            name=orm.name,
        )


@dataclasses.dataclass(eq=False, frozen=True)
class ChartOfAccounts(lib.SyncEntity):
    number: str
    name: str

    @classmethod
    def from_local(cls, orm):
        # Just for fun, we'll be passing an Account instance instead of
        # AccountCode. Account is more commonly used in the codebase than
        # AccountCode.
        return cls(
            local_id=orm.id,
            remote_id=database.AccountCodeObjectMap.retrieve(orm.account_code.id),
            number=orm.account_code.code,
            name=orm.account_code.description,
        )


@dataclasses.dataclass(eq=False, frozen=True)
class Vendor(lib.SyncEntity):
    name: str
    location: Location

    def serialize(self):
        ser = super().serialize()
        ser["location_id"] = self.location.remote_id
        return ser

    @classmethod
    def from_local(cls, orm):
        return cls(
            local_id=orm.id,
            remote_id=database.VendorObjectMap.retrieve(orm.id),
            name=orm.name,
            location=Location.from_local(orm.location),
        )


@dataclasses.dataclass(eq=False, frozen=True)
class Item(lib.SyncEntity):
    description: str
    quantity: int
    rate: int
    total: int
    currency: Currency

    def serialize(self):
        ser = super().serialize()
        print(self.currency)
        ser["currency_id"] = self.currency.remote_id
        return ser

    @classmethod
    def from_local(cls, orm):
        # There will instances where remote system requires a certain attribute
        # that does not exist locally. In those case, we either need to define
        # fallback values or query the main system.
        return cls(
            local_id=orm.id,
            remote_id=None,
            description=orm.description,
            quantity=orm.quantity,
            rate=orm.unit_cost,
            total=orm.total,
            currency=Currency.from_local(orm.currency),
        )


@dataclasses.dataclass(eq=False, frozen=True)
class VendorBill(lib.SyncEntity):
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
                "account_id": self.account.remote_id,
                "vendor_id": self.vendor.remote_id,
                "currency_id": self.currency.remote_id,
                "location_id": self.location.remote_id,
                "department_id": self.department.remote_id,
                "items": [item.serialize() for item in self.items],
            }
        )
        return ser

    @classmethod
    def from_local(cls, orm):
        return cls(
            local_id=orm.id,
            remote_id=database.VendorBillObjectMap.retrieve(orm.id),
            invoice=orm.invoice_number,
            account=ChartOfAccounts.from_local(orm.items[0].account),
            vendor=Vendor.from_local(orm.vendor),
            currency=Currency.from_local(orm.currency),
            location=Location.from_local(orm.items[0].account.department.branch),
            department=Department.from_local(orm.items[0].account.department),
            items=[Item.from_local(item) for item in orm.items],
        )


@dataclasses.dataclass(eq=False, frozen=True)
class BillCollection(lib.SyncEntity):
    """Only used as a container of bills. Does not refer to an entity in the
    remote system.
    """

    bills: typing.List[VendorBill]

    def serialize(self):
        return {"bills": [bill.serialize() for bill in self.bills]}
