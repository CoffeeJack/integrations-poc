#!/usr/bin/env python3
import importlib


def get_backend(name):
    return importlib.import_module(f"integration.backends.{name}")
