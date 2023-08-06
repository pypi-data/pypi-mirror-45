from typing import Dict

import yaml

from ktdk import KTDK
from .base import DeclarativeSuiteLoader, DeclarativeTaskLoader, DeclarativeTestLoader
from .resolvers import Resolver, BuildTaskResolver, ExecuteTaskResolver, FSTasksResolver, \
    TaskBaseResolver, TestBaseResolver


def load_file(path) -> Dict:
    return yaml.safe_load(path)


def load_suite(definition, ktdk: KTDK) -> KTDK:
    return DeclarativeSuiteLoader(definition, ktdk).load()
