#!/usr/bin/env python3
import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class BaseEntity:
    id: int

    def __str__(self):
        return f"<{type(self).__name__} id={self.id}>"


@dataclasses.dataclass(frozen=True)
class Currency(BaseEntity):
    name: str
    rate: float


@dataclasses.dataclass(frozen=True)
class Location(BaseEntity):
    name: str
    localCurrency: Currency


@dataclasses.dataclass(frozen=True)
class Department(BaseEntity):
    name: str
    branch: Location


@dataclasses.dataclass(frozen=True)
class AccountCode(BaseEntity):
    code: str
    description: str


@dataclasses.dataclass(frozen=True)
class Account(BaseEntity):
    account_code: AccountCode
    department: Department


@dataclasses.dataclass(frozen=True)
class Vendor(BaseEntity):
    name: str
    currency: Currency
    location: Location


@dataclasses.dataclass(frozen=True)
class Item(BaseEntity):
    account: Account
    description: str
    quantity: int
    unit_cost: int
    currency: Currency

    @property
    def total(self):
        return self.quantity * self.unit_cost


@dataclasses.dataclass(frozen=True)
class Bill(BaseEntity):
    invoice_number: str
    vendor: Vendor
    currency: Currency
    items: typing.List[Item]
