import pytest
import yaml

from ktdk.declarative import resolvers
from ktdk.tasks.cpp import ValgrindCommand
from ktdk.tasks.raw.executable import ExecutableTask

EXEC_SCHEMA = """
executable: engine
executor: valgrind
input:
    file: simple_test.in
checks:
    - type: stdout
      equals: "Engine works!"
    - type: stderr
      match: 'some regex'
    - type: return_code
      greater: 10
"""


@pytest.fixture
def resolver():
    def _resolve(text):
        return resolvers.ExecuteTaskResolver(yaml.safe_load(text))

    return _resolve


def test_simple_build_resolver(resolver):
    entity = resolver(EXEC_SCHEMA).resolve()
    assert isinstance(entity, ExecutableTask)
    assert entity.executable_name == 'engine'
    assert entity.executor == ValgrindCommand
    assert entity.command_config['input'] == dict(file='simple_test.in')
    assert len(entity.tasks) == 3
