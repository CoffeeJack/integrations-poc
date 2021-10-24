#!/usr/bin/env python3
import importlib


class BackendError(Exception):
    pass


def get_backend(name):
    try:
        return importlib.import_module(f"integration.backends.{name}")
    except ImportError:
        raise BackendError(f"Integration backend '{name}' does not exist.")
