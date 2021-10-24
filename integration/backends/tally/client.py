#!/usr/bin/env python3
from integration import lib
from integration.backends.tally import server


class Client(lib.Client):
    def send(self, body) -> lib.Response:
        status, _body = server.handle_request(
            method="POST",
            route=self.endpoint,
            body=body,
        )
        response = lib.Response(status=status, body=_body)
        return response

    def retrieve(self, key) -> lib.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/{key}"
        )
        response = lib.Response(status=status, body=body)
        return response

    def search(self, key: str, value: str) -> lib.Response:
        status, body = server.handle_request(
            method="GET", route=f"{self.endpoint}/?{key}={value}"
        )
        response = lib.Response(status=status, body=body)
        return response
