from pathlib import Path

import pytest
from autohooks.config import load_config_from_pyproject_toml, AutohooksConfig, Config

from autohooks.plugins.autopep8.autopep8 import *


def get_test_config_path(
        name):
    return Path(
        __file__).parent / name


@pytest.fixture
def conf1() -> Config:
    config_path = get_test_config_path(
        'test_config_1.toml')
    assert config_path.is_file()

    return load_config_from_pyproject_toml(config_path).get_config()


@pytest.fixture
def conf2() -> Config:
    config_path = get_test_config_path('test_config_2.toml')
    assert config_path.is_file()

    return load_config_from_pyproject_toml(config_path).get_config()


@pytest.fixture
def conf3() -> Config:
    config_path = get_test_config_path('test_config_3.toml')
    assert config_path.is_file()

    return load_config_from_pyproject_toml(config_path).get_config()


def test_include_from_config(conf1):
    l = list(get_include_from_config(conf1))
    assert '1.py' in l
    assert 'foo/2.py' in l
    assert len(l) == 2


def test_include_default(conf2):
    assert list(get_include_from_config(conf2)) == ['*.py']


def test_experimental_features_from_config(conf1):
    assert get_experimental_features_from_config(conf1) is True


def test_experimental_features_default(conf2):
    assert get_experimental_features_from_config(conf2) is False


def test_ignore_errors_from_config(conf1):
    l = list(get_ignore_errors_from_config(conf1))
    assert 'E101' in l
    assert 'E102' in l
    assert len(l) == 2


def test_ignore_errors_default(conf2):
    l = list(get_ignore_errors_from_config(conf2))
    assert 'E226' in l
    assert 'E24' in l
    assert 'W50' in l
    assert 'W690' in l
    assert len(l) == 4


def test_default_line_length_from_config(conf1):
    assert get_default_line_length_from_config(conf1) == 20


def test_default_line_length_default(conf2):
    assert get_default_line_length_from_config(conf2) == 79


def test_autopep8_call_conf2(conf2):
    assert precommit(conf2) == 0


