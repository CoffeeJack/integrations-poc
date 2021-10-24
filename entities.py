#!/usr/bin/env python3
import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class Currency:
    id: int
    name: str
    rate: float


@dataclasses.dataclass(frozen=True)
class Location:
    id: str
    name: str
    localCurrency: Currency


@dataclasses.dataclass(frozen=True)
class Department:
    id: str
    name: str
    branch: Location


@dataclasses.dataclass(frozen=True)
class AccountCode:
    id: int
    code: str
    description: str


@dataclasses.dataclass(frozen=True)
class Account:
    id: int
    account_code: AccountCode
    department: Department


@dataclasses.dataclass(frozen=True)
class Vendor:
    id: int
    name: str
    currency: Currency


@dataclasses.dataclass(frozen=True)
class Item:
    id: int
    account: Account
    description: str
    quantity: int
    unit_cost: int

    @property
    def total(self):
        return self.quantity * self.unit_cost


@dataclasses.dataclass(frozen=True)
class Bill:
    invoice_number: str
    vendor: Vendor
    currency: Currency
    items: typing.List[Item]
