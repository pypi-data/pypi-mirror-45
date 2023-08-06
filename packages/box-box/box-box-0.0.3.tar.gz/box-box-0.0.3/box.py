import logging
from collections import defaultdict
from functools import partial
from typing import Dict, Set

import pkg_resources


class Box:
    store: Dict[str, dict] = defaultdict(dict)
    searched: Set[str] = set()

    @classmethod
    def exist(cls, name: str, tag: str = None) -> bool:
        return name in cls.list(tag=tag)

    @classmethod
    def load(cls, name: str, default=None, tag: str = None):
        return cls.list(tag=tag).get(name, default)

    @classmethod
    def erase(cls, name: str, tag: str = None) -> None:
        if cls.exist(name, tag):
            cls.list(tag=tag).pop(name)

    @classmethod
    def register(cls, obj, name: str = None, tag: str = None):
        if name is None:
            name = obj.__name__
        if cls.exist(name):
            logging.getLogger('box').warning(f'Model [{name}] exists and will be replaced with [{obj}]')
        cls.list(tag=tag)[name] = obj

        return obj

    @classmethod
    def list(cls, tag: str = None) -> dict:
        group_name = f'sf.box.{tag or "default"}'
        if group_name not in cls.searched:
            cls.searched.add(group_name)
            for entry_point in pkg_resources.iter_entry_points(group_name):
                entry_point.resolve()  # pragma: no cover
        return cls.store[tag]


def register(obj=None, name: str = None, tag: str = None):
    """
    Register a class with tag, use in decorator
    :param obj: required
    :param name: class name in default
    :param tag: None in default
    :return: class it self
    """
    if obj is None:
        return partial(Box.register, name=name, tag=tag)
    else:
        return Box.register(obj=obj, name=name, tag=tag)


def factory(config: dict, tag: str = None):
    """
    Object factory, from config to object
    :param config: yaml or json config
    :param tag: string
    :return: object
    """
    type = config['type']
    class_type = Box.load(name=type, tag=tag)
    assert class_type is not None, f'Class [{type}] Not Found!'
    return class_type.factory(config=config)


load = Box.load
erase = Box.erase
