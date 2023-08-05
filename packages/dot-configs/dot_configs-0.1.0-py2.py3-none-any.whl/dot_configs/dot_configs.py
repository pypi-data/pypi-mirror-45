#!/usr/bin/env python3

# Imports
from os import path
import json
from collections import MutableMapping


class NoneWrapper:
    def __init__(self, value):
        self.value = None

    def __name__(self):
        return str(None)

    def __str__(self):
        return str(None)

    def __repr__(self):
        return str(None)

class IntWrapper(int):
    def __init__(self, value):
        super().__init__()

class FloatWrapper(float):
    def __init__(self, value):
        super().__init__()

class StrWrapper(str):
    def __init__(self, value):
        super().__init__()

class ListWrapper(list):
    def __init__(self, value):
        super().__init__(value)

class TupleWrapper(tuple):
    def __init__(self, value):
        super().__init__()

class BoolWrapper(int):
    def __init__(self, value):
        super().__init__()


class AttributeWrapper(MutableMapping):
    """TODO: Docstring for AttributeWrapper."""

    wrappers = {"int": IntWrapper,
                "IntWrapper": IntWrapper,
                "float": FloatWrapper,
                "FloatWrapper": FloatWrapper,
                "str": StrWrapper,
                "StrWrapper": StrWrapper,
                "list": ListWrapper,
                "ListWrapper": ListWrapper,
                "tuple": TupleWrapper,
                "TupleWrapper": TupleWrapper,
                "bool": IntWrapper,
                "BoolWrapper": IntWrapper,
                "NoneType": NoneWrapper
                }

    def __init__(self, key, *args, **kwargs):
        self.key = key
        self._store = {}

    def set(self, key, *args):
        if not args:
            # 1
            aw = AttributeWrapper(key)
            self._store[key] = aw
            setattr(self, aw.key, aw)
            setattr(aw, '_previous', self)
            #  print("1: ", type(aw))
        else:
            # 2
            value = args[0]
            if isinstance(value, dict):
                #  print("3: ", self.key)
                # 3: type AttributeWrapper
                aw = AttributeWrapper(key)
                aw._store = value
                setattr(aw, '_previous', self)
                setattr(self, aw.key, aw)
            else:
                # 4: Str/Float/List/../Wrapper
                #  aw = AttributeWrapper.wrappers[str(type(value))](value)
                aw = AttributeWrapper.wrappers[value.__class__.__name__](value)
                self._store[key] = value
                #  setattr(self, key, type(value)(aw))
                setattr(self, key, aw)
                setattr(aw, '_previous', self)

    def deep_get(self, *args):
        if not args:
            # Nothing in list
            return self
        else:
            l = args[0]
            if len(l) == 1 and not isinstance(l[0], dict):
                return getattr(self, l[0])
            elif len(l) == 1 and isinstance(l[0], dict):
                return l[0]
            elif l:
                try:
                    # if list item is object, take the key
                    l[0] = l[0].key
                except:
                    pass
                try:
                    #  return getattr(self, l[0].key).deep_get(l[1:])
                    return getattr(self, l[0]).deep_get(l[1:])
                except AttributeError as e:
                    # Reached TypeWrapper
                    print(e)
                    #  return getattr(self, l[0]).deep_get(l[1:])
            else:
                # Only AttributeWrappers in list
                return self

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return str(self._store)

class Configurations():
    """Object holding configuration variables."""

    def __init__(self, config_file):
        self.configuration = AttributeWrapper("configurations")
        self.json_validated = False
        cf = path.abspath(config_file)
        configs = self._import_configs(cf)
        self.configuration._store = configs
        self.configuration._previous = None
        self._parse_json(configs)

    @property
    def validated(self):
        return self.json_validated

    def get_configuration(self):
        """docstring for get_configuration"""
        return self.configuration

    def _import_configs(self, conf_file):
        """Import configurations from tf_conf.json."""
        try:
            with open(str(conf_file), 'r') as infile:
                conf = json.load(infile)
            self.json_validated = True
            return conf
        except ValueError as e:
            print("Decoding the JSON config file has failed. Please make sure the format is correct.")
            self.json_validated = False
            #  return None

    def _parse_json(self, sub_tree, prev_node=None, prev_key=None):
        """Parses json object recursively and returns path and value."""

        if isinstance(sub_tree, dict):
            for key, value in sub_tree.items():

                try:
                    curr_node = getattr(prev_node, prev_key)
                except TypeError as e:
                    curr_node = self.configuration

                curr_node.set(key, value)
                self._parse_json(value, curr_node, key)
        else:
            try:
                prev_node.set(prev_key, sub_tree)
            except Exception as e:
                print(e)
