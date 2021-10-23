#!/usr/bin/env python3
import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class SyncEntity:
    """
    This abstract class is an interface for "syncable" entities. It should
    be implemented for each model that needs to be synced with an external
    system.
    """

    local_id: int
    remote_id: typing.Optional[int]

    def __eq__(self, other):
        return (
            type(self).__name__ == type(other).__name__
            and self.local_id == other.local_id
        )

    def serialize(self):
        return {"local_id": self.local_id, "remote_id": self.remote_id}

    @classmethod
    def deserialize(cls, data):
        if "id" in data:
            data["remote_id"] = data["id"]
            del data["id"]
        return cls(**data)


@dataclasses.dataclass(eq=False, frozen=True)
class Currency(SyncEntity):
    code: str

    def serialize(self):
        ser = super().serialize()
        ser.update({"code": self.code})
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class Location(SyncEntity):
    name: str

    def serialize(self):
        ser = super().serialize()
        ser.update(
            {"name": self.name, "local_id": self.local_id, "remote_id": self.remote_id}
        )
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class Department(SyncEntity):
    name: str

    def serialize(self):
        ser = super().serialize()
        ser.update({"name": self.name})
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class Account(SyncEntity):
    code: str
    location: Location
    department: Department

    def serialize(self):
        ser = super().serialize()
        ser.update(
            {
                "code": self.code,
                "location": self.location.serialize(),
                "department": self.department.serialize(),
            }
        )
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class Vendor(SyncEntity):
    name: str
    currency: Currency

    def serialize(self):
        ser = super().serialize()
        ser.update({"name": self.name, "currency": self.currency.serialize()})
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class BillItem(SyncEntity):
    account: Account
    name: str
    quantity: int
    unit_cost: int
    currency: Currency

    def serialize(self):
        ser = super().serialize()
        ser.update(
            {
                "account": self.account.serialize(),
                "name": self.name,
                "quantity": self.quantity,
                "unit_cost": self.unit_cost,
                "currency": self.currency.serialize(),
            }
        )
        return ser

    def deserialize(data):
        return BillItem(**data)


@dataclasses.dataclass(eq=False, frozen=True)
class Bill(SyncEntity):
    vendor: Vendor
    invoice_number: str
    items: typing.List[BillItem]

    def serialize(self):
        ser = super().serialize()
        ser.update(
            {
                "vendor": self.vendor.serialize(),
                "invoice_number": self.invoice_number,
                "items": [item.serialize() for item in self.items],
            }
        )
        return ser


@dataclasses.dataclass(eq=False, frozen=True)
class BillCollection(SyncEntity):
    """Only used as a container of bills. Does not refer to an entity in the
    remote system.
    """

    bills: typing.List[Bill]

    def serialize(self):
        return {"bills": [bill.serialize() for bill in self.bills]}
