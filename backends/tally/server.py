#!/usr/bin/env python3

import re
import enum
import typing
import dataclasses
from urllib import parse

from integrations import lib


__all__ = ["handle_request"]


############
# Database #
############


CurrencyStore = lib.Datastore(
    name="Currency",
    fields=(
        "id",
        "name",
        "iso_code",
    ),
)

LocationStore = lib.Datastore(
    name="Location",
    fields=(
        "id",
        "name",
    ),
)

DepartmentStore = lib.Datastore(
    name="Department",
    fields=(
        "id",
        "name",
    ),
)

ChartOfAccountsStore = lib.Datastore(
    name="Chart of Accounts",
    fields=(
        "id",
        "number",
        "name",
    ),
)

VendorStore = lib.Datastore(
    name="Vendor",
    fields=(
        "id",
        "name",
        "location_id",
    ),
)

VendorBillStore = lib.Datastore(
    name="Vendor Bill",
    fields=(
        "id",
        "acccount_id",
        "vendor_id",
        "currency_id",
        "location_id",
        "items",
    ),
)


#######
# API #
#######


class MethodNotSupportedError(Exception):
    pass


class API:
    store: lib.Datastore

    def get(self, key: str, value: str):
        """Fetch a record from the datastore.

        Args:
            key: Key to use when looking up the value. It must be a valid
                 attribute of the entity.
            value: Value for the given key.

        """
        if key == self.store.pk:
            # Simple lookup by the key
            try:
                record = self.store.retrieve(value)
            except lib.DatastoreException as e:
                return (404, {"error": str(e)})
            return (200, record)
        else:
            # Search by key/value pair
            records = self.store.retrieve()
            for record in records:
                if record.get(key, None) == value:
                    return (200, record)

        return (404, {"error": f"Could not find entity with '{key}={value}'"})

    def post(self, body: dict):
        try:
            record = self.store.save(body)
        except lib.DatastoreException as e:
            return (400, {"error": str(e)})
        return (200, record)


class LocationAPI(API):
    store = LocationStore

    def post(self, body):
        raise MethodNotSupportedError()


class DepartmentAPI(API):
    store = DepartmentStore

    def post(self, body):
        raise MethodNotSupportedError()


class CurrencyAPI(API):
    store = CurrencyStore

    def post(self, body):
        raise MethodNotSupportedError()


class ChartOfAccountsAPI(API):
    store = ChartOfAccountsStore

    def post(self, body):
        raise MethodNotSupportedError()


class VendorAPI(API):
    store = VendorStore


class VendorBillAPI(API):
    store = VendorBillStore


###########
# Routing #
###########


class RequestMethod(enum.Enum):
    GET = "get"
    POST = "post"


@dataclasses.dataclass
class Route:
    pattern: str
    api_class: typing.Type[API]


class Router:
    routes: typing.Dict[str, Route]

    def __init__(self):
        self.routes = {}

    def register(self, pattern: str, api_class: typing.Type[API]):
        route = Route(pattern=pattern, api_class=api_class)
        self.routes[route.pattern] = route

    def find(self, route: str) -> Route:
        for _route in self.routes.keys():
            patt = re.compile(_route)
            if patt.match(route):
                return self.routes[_route]

        raise ValueError("Route not found.")


router = Router()
router.register(r"/currencies/(\w+)?", CurrencyAPI)
router.register(r"/locations/(\w+)?", LocationAPI)
router.register(r"/departments/(\w+)?", DepartmentAPI)
router.register(r"/accounts/(\w+)?", ChartOfAccountsAPI)
router.register(r"/vendors$", VendorAPI)
router.register(r"/vendors/(\w+)?", VendorAPI)
router.register(r"/vendorbills$", VendorBillAPI)
router.register(r"/vendorbills/(\w+)?", VendorBillAPI)


#######################
# HTTP Call Simulator #
#######################


def handle_request(
    method: str, route: str, body: typing.Optional[dict] = None
) -> typing.Tuple[int, dict]:
    method_enum = RequestMethod(method.lower())

    if body is None:
        body = {}

    _route = router.find(route)
    api = _route.api_class()
    api_method = getattr(api, method_enum.value, None)

    if api_method is None:
        raise ValueError("This method is not supported.")

    if method_enum == RequestMethod.GET:
        match = re.compile(_route.pattern).match(route)
        if match is None or not match.groups():
            raise ValueError(f"URL route matching '{route}' not found.")

        group = match.groups()[0]
        if group is not None:
            params = match.groups()
            key = api.store.pk
            value = params[0]
        else:
            # Convert ?foo=bar to key=foo, value=bar
            qs = parse.urlparse(route).query
            key, value = parse.parse_qsl(qs)[0]

        return api_method(key=key, value=value)

    elif method_enum == RequestMethod.POST:
        return api_method(body)

    raise ValueError("Invalid Request")
