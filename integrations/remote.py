#!/usr/bin/env python3
import re
import enum
import typing
import dataclasses

DepartmentStore: typing.List[dict] = []
LocationStore: typing.List[dict] = []
CurrencyStore: typing.List[dict] = []
AccountStore: typing.List[dict] = []
VendorStore: typing.List[dict] = []
BillStore: typing.List[dict] = []


class API:
    store: typing.List[dict] = []

    def get(self, id: int):
        id -= 1000
        return (200, self.store[id])

    def post(self, body: dict):
        self.store.append(body)
        id = len(self.store) + 1000
        body["id"] = id
        return (200, body)


class VendorAPI(API):
    store = VendorStore


class LocationAPI(API):
    store = LocationStore


class DepartmentAPI(API):
    store = DepartmentStore


class CurrencyAPI(API):
    store = CurrencyStore


class AccountAPI(API):
    store = AccountStore


class BillAPI(API):
    store = BillStore


###


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
router.register(r"/vendors$", VendorAPI)
router.register(r"/vendors/(\d+)$", VendorAPI)
router.register(r"/locations$", LocationAPI)
router.register(r"/locations/(\d+)$", LocationAPI)
router.register(r"/departments$", DepartmentAPI)
router.register(r"/departments/(\d+)$", DepartmentAPI)
router.register(r"/currencies$", CurrencyAPI)
router.register(r"/currencies/(\d+)$", CurrencyAPI)
router.register(r"/accounts$", AccountAPI)
router.register(r"/accounts/(\d+)$", AccountAPI)
router.register(r"/bills$", BillAPI)
router.register(r"/bills/(\d+)$", BillAPI)


###


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
        assert match is not None

        params = match.groups()
        if not params:
            raise ValueError("Required route param is missing.")

        param = params[0]
        return api_method(int(param))

    elif method_enum == RequestMethod.POST:
        return api_method(body)

    raise ValueError("Invalid Request")
