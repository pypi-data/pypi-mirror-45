"""pytest options that can be used as test fixtures"""

from collections import namedtuple
from pathlib import Path
import json
from typing import List
import pytest


Option = namedtuple("Option", (
    "type",
    "name",
    "help",
    "default",
    "scope"))

OPTION_DEFAULTS = (str, None, None, None, "module")
Option.__new__.__defaults__ = OPTION_DEFAULTS  # type: ignore


ConfigOption = namedtuple("ConfigOption", (
    "name",
    "help",
    "default",
    "searchpath"))


def _register_as_fixture_function(
        option: Option,
        fixture_function,
        globals_,
        parser):
    fixture_function.__name__ = option.name.replace("-", "_")
    fixture_function.__doc__ = option.help
    fixture = pytest.fixture(scope=option.scope)(fixture_function)
    assert option.name not in globals_
    globals_[option.name] = fixture
    parser.addoption(
        "--" + option.name,
        action="store",
        help=option.help,
        type=option.type,
        default=option.default
    )
    return fixture_function


def _register_as_fixture(option: Option, globals_, parser):
    def fixture_function(request):
        return request.config.getoption("--" + option.name)
    return _register_as_fixture_function(
        option=option,
        globals_=globals_,
        parser=parser,
        fixture_function=fixture_function)


def register(
        globals_,
        parser,
        options: List[Option]):
    """add options to pytest that can be used as test fixtures"""
    for opt in options:
        _register_as_fixture(opt, globals_, parser)