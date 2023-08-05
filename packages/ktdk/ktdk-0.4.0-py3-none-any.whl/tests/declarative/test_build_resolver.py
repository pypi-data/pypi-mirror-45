import pytest
import yaml

from ktdk.core.tasks import TaskType
from ktdk.declarative import resolvers
from ktdk.tasks import cpp

BUILD_SCHEMA = """
tool: c_raw
executable: hello
# Files are relative to workspace
files:
  - hello.c
required: true
"""


@pytest.fixture
def resolver():
    def _resolve(text):
        return resolvers.BuildTaskResolver(yaml.safe_load(text))

    return _resolve


def test_simple_build_resolver(resolver):
    entity = resolver(BUILD_SCHEMA).resolve()
    assert isinstance(entity, cpp.compiler.CCompilerTask)
    assert entity.executable == 'hello'
    assert entity.files == ['hello.c']
    assert entity.type == TaskType.REQUIRED
