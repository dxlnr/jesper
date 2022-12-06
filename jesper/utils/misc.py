"""Miscellaneous Helper Functions"""
from pathlib import Path
from typing import Dict


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def findkeys(node: Dict, kv: str):
    """Finds key in nested dictionary.
    
    :param node: Dictionary to search the key.
    :param kv: Key to search for.
    """
    if isinstance(node, dict):
        if kv in node:
            return node[kv]
        for j in node.values():
            if j is None:
                return None
            else:
                for x in findkeys(j, kv):
                    return x


def find(key, value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find(key, d):
                        yield result


import itertools


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)
