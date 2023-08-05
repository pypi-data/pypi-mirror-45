import pytest
import yaml

from ktdk import KTDK, declarative

HELLO_DEF = """
config:
    timeout: 20
tags:
    - naostro
    - nanecisto

suite:
    name: hello
    description: Hello world intro program
    tasks:
        - fs:
            tool: exist
            submission:
                - 'hello.c'
            test_files:
                - 'solution.c'
            required: true
            
        - fs:
              tool: copy
              submission:
                  - 'hello.c'
              test_files:
                  - pattern: 'solution.c'
        - build:
            tool: c_raw
            executable: student_hello
            files:
                - hello.c
            required: true
        - build:
            tool: c_raw
            executable: teacher_hello
            files:
                - solution.c
            required: true
    tests:
        - name: student_hello
          description: Student's hello should write hello
          tags:
            - naostro
          tasks:
            - execute:
                executable: student_hello
                executor: valgrind
                checks:
                    - type: stdout
                      regex: 'Hello World!'
                    - type: stderr
                      equals: ''
                    - type: return_code
                      equals: 0
                      
        - name: teacher_hello
          description: Teacher's hello should write hello
          tags:
           - nanecisto
          tasks:
            - execute:
                executable: teacher_hello
                executor: valgrind
                checks:
                    - type: stdout
                      regex: 'Hello World!'
                    - type: stderr
                      equals: ''
                    - type: return_code
                      equals: 0
"""


def create_file(where, name, content=None):
    default = (
        """#include <stdio.h>

int main() {
  printf("Hello World!\\n");
  return 0;
}""")
    content = content or default
    path = where.join(f'{name}.c')
    path.write(content)
    return path


@pytest.fixture
def workspace_dir(tmpdir):
    workspace = tmpdir.mkdir('workspace')
    return workspace


@pytest.fixture
def test_files_dir(tmpdir):
    test_files = tmpdir.mkdir('test_files')
    return test_files


@pytest.fixture
def submission_dir(tmpdir):
    submission = tmpdir.mkdir('submission')
    return submission


@pytest.fixture()
def prepared_sources(submission_dir, test_files_dir):
    create_file(submission_dir, 'hello')
    create_file(test_files_dir, 'solution')
    return submission_dir


@pytest.fixture()
def ktdk(workspace_dir, test_files_dir, submission_dir) -> KTDK:
    ktdk = KTDK(
        test_files=test_files_dir,
        submission=submission_dir,
        workspace=workspace_dir
    )

    return declarative.load_suite(yaml.safe_load(HELLO_DEF), ktdk)


def test_decl_hello_test(ktdk, prepared_sources):
    ktdk.invoke()
    assert ktdk.suite.result.effective.passed
