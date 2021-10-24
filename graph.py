#!/usr/bin/env python3
import typing
from integrations import lib


class Node:
    def __init__(
        self,
        entity: lib.SyncEntity,
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
            return
        self.is_visited = True


def generate_graph(root: lib.SyncEntity, cache=None):
    if cache is None:
        cache = {}

    if root in cache:
        node = cache[root]
    else:
        node = Node(entity=root)
        cache[node.entity] = node

    for field_name, field in root.__dataclass_fields__.items():
        if typing.get_origin(field.type) is list:
            # Handle list of dependenecies
            for item in getattr(root, field_name):
                dep = generate_graph(item, cache)
                node.add_dependency(dep)
        elif typing.get_origin(field.type) is typing.Union:
            # Handle optional dependency
            item = getattr(root, field_name)
            if item is not None:
                dep = generate_graph(item, cache)
                node.add_dependency(dep)
        elif issubclass(field.type, lib.SyncEntity):
            # Base case
            dep = generate_graph(getattr(root, field_name), cache)
            node.add_dependency(dep)

    return node


def resolve_dependencies(node: Node):
    """
    Run depth first search on the given root of graph and produces a list
    of entities in the order in which those should be synced.
    """

    resolution = []
    stack = [node]
    while stack:
        current = stack.pop(0)
        if current.deps:
            for dep in current.deps:
                if isinstance(dep, list):
                    stack.extend(dep)
                else:
                    stack.append(dep)
        resolution.append(current)

    unique = []
    while resolution:
        node = resolution.pop()
        if node in unique:
            continue
        node.visit()
        unique.append(node)

    return [node.entity for node in unique]
