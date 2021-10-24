#!/usr/bin/env python3
import typing
from integrations import logger
from integrations.backends import entities


class Node:
    def __init__(
        self,
        entity: entities.SyncEntity,
        deps: typing.Optional[typing.List["Node"]] = None,
    ):
        self.entity = entity
        self.deps = deps if deps is not None else []
        self.is_visited = False

    def __repr__(self):
        return f"<Node {type(self.entity).__name__}={self.entity.local_id}>"

    def add_dependency(self, dep: "Node"):
        if dep not in self.deps:
            self.deps.append(dep)

    def visit(self):
        if self.is_visited:
            logger.debug(f"Already synced {self}.")
            return

        self.is_visited = True
        logger.debug(f"Syncing {self}.")

        # This is where the magic happens or supposed to happen
        # client.sync(self.entity)


def generate_graph(root: entities.SyncEntity, cache=None):
    if cache is None:
        cache = {}

    if root in cache:
        node = cache[root]
    else:
        node = Node(entity=root)
        cache[node.entity] = node

    for field_name, field in root.__dataclass_fields__.items():
        if hasattr(field.type, "__origin__"):
            if field.type.__origin__ is list:
                for item in getattr(root, field_name):
                    dep = generate_graph(item, cache)
                    node.add_dependency(dep)
        elif issubclass(field.type, entities.SyncEntity):
            dep = generate_graph(getattr(root, field_name), cache)
            node.add_dependency(dep)
    return node


def depth_first_search(node: Node):
    dependency_resolution = []
    stack = [node]
    while len(stack):
        current = stack.pop(0)
        if current.deps:
            for dep in current.deps:
                if isinstance(dep, list):
                    stack.extend(dep)
                else:
                    stack.append(dep)

        dependency_resolution.append(current)

    while dependency_resolution:
        node = dependency_resolution.pop()
        node.visit()
