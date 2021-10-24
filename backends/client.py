#!/usr/bin/env python3

import abc
import typing
import dataclasses


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
