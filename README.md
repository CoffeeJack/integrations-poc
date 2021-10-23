# Integrations PoC

This is proof-of-concept project that demonstrates usage of a directed graph to
resolve dependencies and sync with a remote systems.

# Usage

There are three main components:

- Entities: These refer to objects that can be synced with a remote system.
- Graph: Represented as adjacency list this module contains function to generate
  graph and traverse it using depth first search.
- Remote: This is essential a stub simulating the remote system.

See `main.py` for example usage.
