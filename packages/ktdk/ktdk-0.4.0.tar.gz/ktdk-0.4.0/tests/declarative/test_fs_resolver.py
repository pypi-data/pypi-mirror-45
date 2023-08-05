import pytest
import yaml

from ktdk.declarative import resolvers
from ktdk.tasks.fs import CopyFiles

FS_SCHEMA = """
tool: copy
test_files:
  - '*.c'
  - '../*.h'
submission:
  - pattern: '*.c'
    output_subdir: 'src'
"""


@pytest.fixture
def resolver():
    def _resolve(text):
        return resolvers.FSTasksResolver(yaml.safe_load(text))

    return _resolve


def test_simple_fs_resolver(resolver):
    entity = resolver(FS_SCHEMA).resolve()
    assert isinstance(entity, list)
    assert len(entity) == 3

    test_files0 = entity[0]
    assert isinstance(test_files0, CopyFiles)
    assert test_files0.pattern == ['*.c']

    test_files1 = entity[1]
    assert isinstance(test_files1, CopyFiles)
    assert test_files1.pattern == ['../*.h']

    submission = entity[2]
    assert isinstance(submission, CopyFiles)
    assert submission.pattern == ['*.c']
    assert submission.output_subdir == 'src'
