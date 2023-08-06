from typing import Type

from ktdk import tasks
from ktdk.asserts.checks import *
from ktdk.asserts.matchers import *
from ktdk.core.mixins import ExecutorMixin
from ktdk.tasks.fs.tasks import *


def full() -> Dict[str, Dict[str, Type]]:
    return {
        'build': build(),
        'checks': checks(),
        'file_tools': fs_tools(),
        'executors': executors(),
        'matchers': matchers(),
        'resolvers': resolvers()
    }


def build() -> Dict:
    return tasks.build_task.BuildTask.tools_register()


def checks() -> Dict:
    return CheckTask.check_register()


def fs_tools() -> Dict:
    return tasks.fs.AbstractFilesTask.tools_register()


def executors() -> Dict:
    return ExecutorMixin.exec_register()


def matchers() -> Dict:
    return GeneralMatcher.matchers_register()


def resolvers() -> Dict:
    from . import resolvers
    return resolvers.Resolver.registered()


def resolvers_base() -> Dict:
    from . import resolvers
    return resolvers.BaseAttributeResolver.base_attr_resolvers()


def resolvers_task_attribute() -> Dict:
    from . import resolvers
    return resolvers.TaskAttributeResolver.task_attr_resolvers()


def resolvers_test_attribute() -> Dict:
    from . import resolvers
    return resolvers.TestAttributeResolver.test_attr_resolvers()


def resolvers_task_type() -> Dict:
    from . import resolvers
    return resolvers.TaskTypeResolver.task_type_resolvers()


def fs_tool_get(name: str):
    return fs_tools().get(name)


def checks_get(name: str):
    return checks().get(name)


def build_get(name: str):
    return build().get(name)


def executor_get(name: str):
    return executors().get(name)


def resolver_get(name):
    return resolvers().get(name)


def resolver_base_get(key):
    return resolvers_base().get(key)


def resolver_test_attr_get(key):
    return resolvers_test_attribute().get(key)


def resolver_task_attr_get(key):
    return resolvers_task_attribute().get(key)


def resolver_task_type_get(key):
    return resolvers_task_type().get(key)
