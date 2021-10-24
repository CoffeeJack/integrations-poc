#!/usr/bin/env python3

import abc
import enum
import random
import typing
import string
import threading
import dataclasses


class DatastoreException(Exception):
    pass


class Datastore:
    __storage: typing.Dict[str, dict]
    __lock: threading.Lock

    def __init__(
        self,
        name: str,
        fields: typing.Tuple[str, ...],
        pk: str = "id",
        keyspace: str = string.ascii_lowercase + string.digits,
    ):
        self.name = name
        self.fields = fields
        self.pk = pk
        self.keyspace = keyspace

        self.__storage = {}
        self.__lock = threading.Lock()

    def __repr__(self):
        record_count = len(self.__storage)
        record_plural = "s" if record_count != 1 else ""
        return f"<{self.name.title()} Datastore: {record_count} record{record_plural}>"

    def _generate_key(self, length=6) -> str:
        out = "".join(random.choice(self.keyspace) for i in range(length))
        return out.lower()

    def _validate_body(self, body):
        if not isinstance(body, dict):
            raise DatastoreException("Values must of 'dict' type.")

        body_fields = body.keys()
        for field in self.fields:
            if field == self.pk:
                continue
            elif field not in body_fields:
                raise DatastoreException(f"Required field '{field}' is missing.")

    def retrieve(self, key: typing.Optional[str] = None, raise_exception=False):
        if key is None:
            if not self.__lock.locked():
                return list(self.__storage.values())

        if key not in self.__storage:
            if raise_exception:
                raise DatastoreException(
                    f"Key '{key}' does not exist in {self.name} datastore."
                )
            return None
        if not self.__lock.locked():
            return self.__storage.get(key)

        raise DatastoreException("Record is locked. Please try again.")

    def save(self, body: dict) -> str:
        self._validate_body(body)
        self.__lock.acquire()

        if self.pk in body:
            key: str = body[self.pk]
        else:
            key = self._generate_key()
            body[self.pk] = key

        self.__storage[key] = body
        self.__lock.release()
        return key

    def remove(self, key) -> None:
        self.__lock.acquire()
        try:
            del self.__storage[key]
        except KeyError:
            pass
        self.__lock.release()

    def reset(self) -> None:
        self.__lock.acquire()
        self.__storage = {}
        self.__lock.release()


ORM = typing.TypeVar("ORM")


@dataclasses.dataclass(frozen=True)
class SyncEntity:
    """
    This is an interface for "syncable" entities. It should be implemented for
    each model that needs to be synced with an external system.
    """

    local_id: int
    remote_id: typing.Optional[str]

    def __eq__(self, other):
        return (
            type(self).__name__ == type(other).__name__
            and self.local_id == other.local_id
        )

    def serialize(self):
        """Produces data that is ready to be sent to the remote system."""

        return dataclasses.asdict(self)

    @classmethod
    def deserialize(cls, data):
        """Accepts data from the remote system and instantiates a SyncEntity."""

        return cls(**data)

    def to_local(cls) -> ORM:
        """Create a local entity from instance of SyncEntity."""
        raise NotImplementedError()

    @classmethod
    def from_local(cls, model: ORM) -> "SyncEntity":
        """Accepts serialized data from the local entity. This needs to be
        implemented on a per remote entity basis."""
        raise NotImplementedError()


class SyncStatus(enum.Enum):
    CREATED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    ERROR = 3


@dataclasses.dataclass
class SyncResult:
    status: SyncStatus
    message: str


@dataclasses.dataclass
class Mapping:
    local_remote_entity: typing.Dict[type, type]
    readonly_entity_lookup: typing.Dict[type, str]
    entity_endpoint: typing.Dict[type, str]
    entity_datastore: typing.Dict[type, Datastore]


@dataclasses.dataclass(frozen=True)
class Response:
    status: int
    body: typing.Union[str, dict]


class Client(abc.ABC):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @abc.abstractmethod
    def send(self, body) -> Response:
        raise NotImplementedError()

    @abc.abstractmethod
    def retrieve(self, key) -> Response:
        raise NotImplementedError()

    @abc.abstractmethod
    def search(self, key, value) -> Response:
        raise NotImplementedError()
