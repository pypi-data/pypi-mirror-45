import logging
from typing import Dict, List

from ktdk import KTDK, Task, Test, utils
from ktdk.core import errors
from ktdk.core.reporters import Reporter
from ktdk.declarative import registry
from ktdk.tasks.raw.executable import ExecutableTask

log = logging.getLogger(__name__)


class Resolver:
    SELECTOR = None
    KLASS = None

    @classmethod
    def registered(cls):
        return utils.make_subclasses_register(Resolver, 'SELECTOR')

    def __init__(self, definition: Dict, parent=None):
        self._definition = definition
        self._parent = parent

    @property
    def definition(self):
        return self._definition

    def _resolve(self, klass=None):
        return self.definition

    def _after_resolution(self, entity):
        pass

    def resolve(self):
        klass = self._get_class(self.__class__.KLASS)
        entity = self._resolve(klass)
        self._after_resolution(entity)
        log.debug(f"[RESOLV] Resolved using {self.__class__.__name__}: {entity}")
        return entity

    def _get_class(self, klass):
        if isinstance(self.definition, dict) and 'class' in self.definition.keys():
            klass = utils.load_class(self.definition['class'])
        return klass


class BaseAttributeResolver(Resolver):
    SELECTOR = None

    @classmethod
    def base_attr_resolvers(cls):
        return utils.make_subclasses_register(BaseAttributeResolver, 'SELECTOR')

    @property
    def ktdk(self) -> KTDK:
        return self._parent


class ConfigResolver(BaseAttributeResolver):
    SELECTOR = 'config'

    def _resolve(self, klass=None):
        self.ktdk.config.update(self.definition)


class TagsResolver(BaseAttributeResolver):
    SELECTOR = 'tags'

    def _resolve(self, klass=None):
        self.ktdk.register_tags(*self.definition)


class ImportsResolver(BaseAttributeResolver):
    SELECTOR = 'imports'

    def _resolve(self, klass=None):
        """TODO: Not implemented now
        """


class ReportersResolver(BaseAttributeResolver):
    SELECTOR = 'reporters'

    def _resolve(self, klass=None):
        for info in self.definition:
            if isinstance(info, str):
                info = dict(name=info)
            self.ktdk.reporters.add(Reporter(**info))


class TestBaseResolver(Resolver):
    SELECTOR = 'test'
    KLASS = Test

    @property
    def _test_params(self) -> Dict:
        excluded = ['before', 'after', 'before_all', 'after_all', 'tasks', 'tests']
        return {key: self.definition[key] for key in self.definition.keys() if key not in excluded}

    def _resolve(self, klass=None):
        return klass(**self._test_params)


class TestAttributeResolver(TestBaseResolver):
    SELECTOR = None

    @classmethod
    def test_attr_resolvers(cls):
        return utils.make_subclasses_register(TestAttributeResolver, 'SELECTOR')


class SuiteResolver(TestBaseResolver):
    SELECTOR = 'suite'


class TaskBaseResolver(Resolver):
    SELECTOR = 'task'
    KLASS = Task

    @property
    def definition(self) -> Dict:
        if len(self._definition.keys()) == 1:
            name = self.__class__.SELECTOR
            return self._definition[name]
        return self._definition

    def _task_params(self, klass) -> Dict:
        params = klass.base_params()
        return {key: self.definition[key] for key in self.definition.keys() if key in params}

    def _resolve(self, klass=None):
        return klass(**self._task_params(klass))

    def _after_resolution(self, entity):
        self._resolve_checks(entity)

    def _resolve_checks(self, task: Task):
        checks = self.definition.get('checks')
        if checks:
            check_list = [_resolve_check(check) for check in checks]
            for check in check_list:
                task.check_that(check)


class TaskAttributeResolver(TaskBaseResolver):
    SELECTOR = None

    @classmethod
    def task_attr_resolvers(cls):
        return utils.make_subclasses_register(TaskAttributeResolver, 'SELECTOR')


class TaskTypeResolver(TaskBaseResolver):
    SELECTOR = None

    @classmethod
    def task_type_resolvers(cls):
        return utils.make_subclasses_register(TaskTypeResolver, 'SELECTOR')


class FSTasksResolver(TaskTypeResolver):
    SELECTOR = 'fs'

    def _resolve_tool(self):
        tool_name = self.definition.get('tool', 'copy')
        tool = registry.fs_tool_get(tool_name)
        if not tool:
            raise errors.DeclRegistryNotFoundError('file tools', tool_name)
        return tool

    def _resolve(self, klass=None):
        tool = self._resolve_tool()
        result = []
        for f_type in ['test_files', 'submission']:
            file_tasks = self._resolve_files(f_type, tool)
            result.extend(file_tasks)
        return result

    def _resolve_files(self, files_type, tool) -> List[Task]:
        result = []
        files_list = self.definition[files_type]
        required = self.definition.get('required') or False
        checked = self.definition.get('checked') or False
        for i, file_item in enumerate(files_list):
            params = {'source': files_type, 'required': required, 'checked': checked}
            if isinstance(file_item, str):
                params['pattern'] = file_item
            else:
                params.update(file_item)
            tool_name = tool.TOOL_NAME
            if isinstance(tool_name, list):
                tool_name = next(iter(tool_name))
            params['name'] = params.get('name', f'{tool_name}_{files_type}_{i}')

            instance = tool(**params)
            result.append(instance)
        return result


class BuildTaskResolver(TaskTypeResolver):
    SELECTOR = 'build'

    def _resolve_tool(self):
        tool_name = self.definition.get('tool')
        tool = registry.build_get(tool_name)
        if not tool:
            raise errors.DeclRegistryNotFoundError('build', tool_name)
        return tool

    def _resolve(self, klass=None) -> Task:
        tool = self._resolve_tool()
        instance = tool(**self._task_params(tool))
        return instance


class ExecuteTaskResolver(TaskTypeResolver):
    SELECTOR = 'execute'

    def _resolve_executor(self):
        tool_name = self.definition.get('executor')
        tool = registry.executor_get(tool_name)
        return tool

    def _resolve(self, klass=None) -> Task:
        executor = self._resolve_executor()
        exec_tool = self._get_class(ExecutableTask)
        params = self._task_params(exec_tool)
        params['executor'] = executor
        instance = exec_tool(**params)
        return instance


def _resolve_matcher(check):
    for (key, val) in check.items():
        item = registry.get_matcher(key)
        if item is not None:
            return item(val) if val is not None else item()
    raise errors.DeclMatcherNotExistError(check)


def _resolve_check(check: Dict):
    check_type = check.get('type')
    if not check_type:
        raise errors.DeclAttributeMissingError('\'type\' for check')

    check_class = registry.checks_get(check_type)

    if check_class is None:
        raise errors.DeclRegistryNotFoundError('checks', check_type)
    matcher = _resolve_matcher(check)

    return check_class(matcher=matcher)
