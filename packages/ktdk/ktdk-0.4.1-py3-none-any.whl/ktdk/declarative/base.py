import logging
from typing import Any, Dict, List, Optional, Union

import yaml

from ktdk import KTDK, Task, Test
from ktdk.core import errors
from ktdk.declarative import registry, resolvers
from ktdk.declarative.yaml_extend import YAMLIncludeLoader, construct_include

yaml.add_constructor('!include', construct_include, YAMLIncludeLoader)

log = logging.getLogger(__name__)


def extract_params(definition: Dict, excluded: List = None):
    excluded = excluded or []
    return {key: definition[key] for key in definition.keys() if key not in excluded}


class DeclarativeBaseLoader:
    KLASS = None
    EXCLUDED_PARAMS = []

    @classmethod
    def klass(cls, *args, **kwargs):
        return cls.KLASS(*args, **kwargs)

    def __init__(self, definition: Dict, throws=False):
        self.definition = definition
        self._throws = throws
        self._errors = []

    def _add_error(self, err):
        log.error(f"[DECL] {err}")
        self._errors.append(err)

    def _resolve_entity(self, param: str = None, resolver=None):
        if resolver is None:
            resolver = registry.resolver_get(param)
        if param is None:
            param = resolver.SELECTOR
        entity = self.definition.get(param)
        if param in self.definition:
            return resolver(entity).resolve()
        return None

    def load(self) -> Any:
        pass


class DeclarativeSuiteLoader(DeclarativeBaseLoader):
    def __init__(self, definition: Dict, ktdk: KTDK):
        super().__init__(definition)
        self._ktdk = ktdk

    @property
    def ktdk(self) -> KTDK:
        return self._ktdk

    def load(self):
        imports = self._resolve_entity(param='imports')
        self._resolve_imports(imports)
        config = self._resolve_entity(param='config')
        self._ktdk.config.update(config, override=True)
        tags = self._resolve_entity(param='tags')
        self._ktdk.register_tags(*tags)
        self._load_suite()
        return self.ktdk

    def _load_suite(self):
        suite_schema = self.definition.get('suite')
        if not suite_schema:
            return None
        suite = DeclarativeTestLoader(definition=suite_schema).load()
        if suite:
            self._ktdk.suite = suite
            log.debug(f"[LOAD] Suite: {suite}")
        return suite

    def _resolve_imports(self, imports):
        pass


def _collect_tasks(collection):
    result = []
    for item in collection:
        loaded = DeclarativeTaskLoader(item).load()
        if isinstance(loaded, Task):
            loaded = [loaded]
        result.extend(loaded)
    return result


class DeclarativeTestLoader(DeclarativeBaseLoader):
    KLASS = Test

    def _create_instance(self) -> Optional[Test]:
        resolver = resolvers.TestBaseResolver
        test_resolvers = resolver.registered()
        if '_type' in self.definition.keys():
            found = test_resolvers.get(self.definition['_type'])
            if found:
                resolver = found
        try:
            test = resolver(self.definition).resolve()
            log.info(f"[LOAD] Test {test}")
            return test
        except errors.DeclarativeError as ex:
            self._add_error(ex)
        return None

    def load(self) -> Optional[Test]:
        if 'test' in self.definition:
            self.definition = self.definition['test']
        test = self._create_instance()
        if test is None:
            return None
        self._add_tasks_if_present(test)
        test.add_test(*self._load_tests())
        return test

    def _add_tasks_if_present(self, test):
        test.add_before(*self._load_tasks('before'))
        test.add_before(*self._load_tasks('before_each'), scope='each')
        test.add_after(*self._load_tasks('after'))
        test.add_before(*self._load_tasks('after_each'), scope='each')
        test.add_task(*self._load_tasks('tasks'))

    def _load_tasks(self, task_type) -> Optional[List[Task]]:
        collection = self.definition.get(task_type)
        if not collection:
            return []
        return _collect_tasks(collection)

    def _load_tests(self) -> Optional[List[Test]]:
        collection = self.definition.get('tests')
        if not collection:
            return []
        return [DeclarativeTestLoader(item).load() for item in collection]


class DeclarativeTaskLoader(DeclarativeBaseLoader):
    KLASS = Task

    TYPES = {}

    def _create_instance(self) -> Optional[Task]:
        resolver = self._get_resolver()
        try:
            task = resolver(self.definition).resolve()
            log.info(f"[LOAD] Task: {task}")
            return task
        except errors.DeclarativeError as ex:
            self._add_error(ex)
        return None

    def _get_resolver(self):
        resolver = resolvers.TaskBaseResolver
        task_resolvers = resolver.registered()
        def_keys = self.definition.keys()
        if len(def_keys) == 1:
            name = next(iter(def_keys))
            found = task_resolvers.get(name)
            if found:
                return found
        if '_type' in self.definition.keys():
            found = task_resolvers.get(self.definition['_type'])
            if found:
                return found
        return resolver

    def load(self) -> Union[Task, List]:
        task = self._create_instance()
        if isinstance(task, Task):
            task.add_task(*self._load_tasks())
            return task
        log.debug("Adding additional task to same level since the result of the resolver is list")
        return [*task, *self._load_tasks()]

    def _load_tasks(self) -> Optional[List[Task]]:
        collection = self.definition.get('tasks')
        if not collection:
            return []
        return _collect_tasks(collection)
