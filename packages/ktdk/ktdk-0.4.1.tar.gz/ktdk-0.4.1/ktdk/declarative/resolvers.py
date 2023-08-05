import logging
from typing import Dict, List

from ktdk import Task, Test, utils
from ktdk.core import errors
from ktdk.declarative import registry
from ktdk.tasks.raw.executable import ExecutableTask

log = logging.getLogger(__name__)


class BaseResolver:
    SELECTOR = None
    BASE_PARAMS = []
    KLASS = None

    @classmethod
    def base_params(cls):
        return utils.bind_class_var(cls, 'BASE_PARAMS')

    @classmethod
    def registered(cls):
        return utils.make_subclasses_register(BaseResolver, 'SELECTOR')

    def __init__(self, definition: Dict):
        self._definition = definition

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


class ConfigResolver(BaseResolver):
    SELECTOR = 'config'


class TagsResolver(BaseResolver):
    SELECTOR = 'tags'


class TestBaseResolver(BaseResolver):
    SELECTOR = 'test'
    KLASS = Test

    @property
    def _test_params(self) -> Dict:
        excluded = ['before', 'after', 'before_all', 'after_all', 'tasks', 'tests']
        return {key: self.definition[key] for key in self.definition.keys() if key not in excluded}

    def _resolve(self, klass=None):
        return klass(**self._test_params)


class SuiteResolver(TestBaseResolver):
    SELECTOR = 'suite'


class TaskBaseResolver(BaseResolver):
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


class FSTasksResolver(TaskBaseResolver):
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


class BuildTaskResolver(TaskBaseResolver):
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


class ExecuteTaskResolver(TaskBaseResolver):
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
