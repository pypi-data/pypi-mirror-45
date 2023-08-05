#!/usr/bin/env python3

"""
Tests for `dot_configs` module.
"""

import pytest
import json
from os import path
from dot_configs.dot_configs import (Configurations, AttributeWrapper)

DATA_JSON_DIR = pytest.DATA_ROOT

@pytest.fixture
def attributewrapper():
    return AttributeWrapper('test')

@pytest.fixture
@pytest.mark.datafiles(DATA_JSON_DIR)
def cfg(datafiles):
    return path.join(str(datafiles), 'conf.json')

@pytest.fixture
@pytest.mark.datafiles(DATA_JSON_DIR)
def cfg_bad(datafiles):
    return path.join(str(datafiles), 'bad.json')

@pytest.fixture
@pytest.mark.datafiles(DATA_JSON_DIR)
def config_dict(cfg):
    with open(cfg, 'r') as infile:
        d = json.load(infile)
    return d

@pytest.fixture
@pytest.mark.datafiles(DATA_JSON_DIR)
def configs(cfg):
    c = Configurations(cfg)
    c = c.get_configuration()
    return c

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_validate_flag_is_true_when_parsing_correctly(cfg):
    c = Configurations(cfg)
    assert c.json_validated is True

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_validate_flag_is_false_when_parsing_incorrectly(cfg_bad):
    c = Configurations(cfg_bad)
    assert c.json_validated is False

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_set_new_node(configs):
    configs.set('args')
    assert isinstance(configs.args, AttributeWrapper)

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_set_new_node_and_value(configs):
    configs.architecture.set('args', 'test')
    assert configs.architecture.args == 'test'

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_deep_get_node_and_value(configs):
    epochs = configs.deep_get(['architecture', 'cnn', 'training_params', 'epochs'])
    assert epochs == 4

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_deep_get_node_only_returns_dict_object(configs, config_dict):
    tp = configs.deep_get(['architecture', 'cnn', 'training_params'])
    assert tp == config_dict["architecture"]["cnn"]["training_params"]

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_int_type_on_attributewrapper(configs):
    assert configs.architecture.cnn.training_params.epochs == 4

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_list_type_on_attributewrapper(configs):
    assert configs.spectrograms.frame_sizes == [1024, 2048, 4096]

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_str_type_on_attributewrapper(configs):
    assert configs.paths.dirs.store == '/path/to/store'

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_float_type_on_attributewrapper(configs):
    assert configs.training_data.test_size == 0.10

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_bool_type_on_attributewrapper(configs):
    assert configs.architecture.cnn.audio_params.filterbank == True

@pytest.mark.skip(reason="Not implemented yet.")
@pytest.mark.datafiles(DATA_JSON_DIR)
def test_none_type_on_attributewrapper(configs):
    assert configs.args is None

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_IntWrapper_behaves_like_int(attributewrapper, configs):
    IntWrapper = attributewrapper.wrappers["int"]
    number = IntWrapper(1)
    assert (number + number) == 2

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_FloatWrapper_behaves_like_float(attributewrapper, configs):
    FloatWrapper = attributewrapper.wrappers["float"]
    number = FloatWrapper(1.2)
    assert (number + number) == 2.4

@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.datafiles(DATA_JSON_DIR)
def test_NoneWrapper_is_None(attributewrapper, configs):
    NoneWrapper = attributewrapper.wrappers["NoneType"]
    none = NoneWrapper("Will result in 'None' anyways")
    assert str(none) == str(None)

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_StrWrapper_behaves_like_str(attributewrapper, configs):
    StrWrapper = attributewrapper.wrappers["str"]
    string = StrWrapper('string')
    assert (string + string) == "stringstring"

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_leaf_on_attributewrapper_is_correct_type(attributewrapper, configs):
    epochs_class = configs.architecture.cnn.training_params.epochs.__class__
    assert isinstance(epochs_class, attributewrapper.wrappers["int"].__class__)

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_attributewrapper_stores_internal_dict_correctly(configs, config_dict):
    assert configs.paths._store == config_dict["paths"]

@pytest.mark.datafiles(DATA_JSON_DIR)
def test_root_attributewrapper_stores_internal_dict_correctly(configs, config_dict):
    assert configs._store == config_dict
