#!/usr/bin/env python3
import typing
import dataclasses
from integrations.lib import Datastore


@dataclasses.dataclass
class Mapping:
    local_remote_entity: typing.Dict[type, type]
    readonly_entity_lookup: typing.Dict[type, str]
    entity_endpoint: typing.Dict[type, str]
    entity_datastore: typing.Dict[type, Datastore]
