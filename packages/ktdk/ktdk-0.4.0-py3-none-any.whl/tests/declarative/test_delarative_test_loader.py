from typing import Dict

import pytest
import yaml

from ktdk import Test, declarative

JUST_TEST_YAML = """
name: just_test
description: 'what ever'
tags: ['some', 'tags']
points: 5
"""

TEST_W_TESTS_YAML = """
name: just_test
description: 'what ever'
tags: ['some', 'tags']
points: 5
tests:
    - name: Foo
      points: 0.5
    - name: Bar
      points: 0.5
"""


@pytest.fixture()
def just_test_definition() -> Dict:
    return yaml.safe_load(JUST_TEST_YAML)


@pytest.fixture()
def test_w_test_definition() -> Dict:
    return yaml.safe_load(TEST_W_TESTS_YAML)


def test_just_test_params_serializer(just_test_definition):
    test_loader = declarative.DeclarativeTestLoader(just_test_definition)
    loaded: Test = test_loader.load()
    assert loaded.name == 'just_test'
    assert loaded.description == 'what ever'
    assert loaded.tags == {'some', 'tags'}
    assert loaded.points == 5


def test_test_with_tests_serializer(test_w_test_definition):
    test_loader = declarative.DeclarativeTestLoader(test_w_test_definition)
    loaded: Test = test_loader.load()
    assert loaded.name == 'just_test'
    assert loaded.description == 'what ever'
    assert loaded.tags == {'some', 'tags'}
    assert loaded.points == 5
    assert len(loaded.tests) == 2
    assert loaded.tests[0].name == 'foo'
    assert loaded.tests[1].name == 'bar'
