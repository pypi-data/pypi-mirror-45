from typing import Dict

from ktdk import utils
from ktdk.core.tasks import Task


class AbortTask(Task):
    def __init__(self, message: str = None, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.description = self.message or message
        self.name = self.name or 'abort_task'

    def _run(self, *args, **kwargs):
        self.asserts.abort(self.message)


class CheckTask(Task):
    CHECK_NAME = None
    BASE_PARAMS = ['matcher', 'output']

    @classmethod
    def check_register(cls) -> Dict:
        return utils.make_subclasses_register(CheckTask, 'CHECK_NAME')

    def __init__(self, matcher=None, **kwargs):
        super().__init__(**kwargs, checked=True)
        self.matcher = matcher

    @property
    def _asserted_object(self):
        return None

    def _run(self, *args, **kwargs):
        self.asserts.check(self._asserted_object, self.matcher)


class TaskResultCheck(CheckTask):
    CHECK_NAME = 'task_result'

    @property
    def _asserted_object(self):
        return self.parent.result.current


class TaskEffectiveResultCheck(CheckTask):
    CHECK_NAME = 'task_result_effective'

    @property
    def _asserted_object(self):
        return self.parent.result.effective


class TestEffectiveResultCheck(CheckTask):
    CHECK_NAME = 'test_result_effective'

    @property
    def _asserted_object(self):
        return self.test.result.effective


class TestResultCheck(CheckTask):
    CHECK_NAME = 'test_result'

    @property
    def _asserted_object(self):
        return self.test.result.current


class AbstractExecResultMatchesTask(CheckTask):
    @property
    def exec_result(self):
        if not self.context:
            return None
        return self.context.config['exec_result']
