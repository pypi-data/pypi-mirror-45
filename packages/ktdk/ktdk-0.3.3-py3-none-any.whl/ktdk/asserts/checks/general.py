from ktdk.core.tasks import Task


class AbortTask(Task):
    def __init__(self, message: str = None, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.desc = self.message or message
        self.name = self.name or 'abort_task'

    def _run(self, *args, **kwargs):
        self.asserts.abort(self.message)


class AbstractMatchesTask(Task):
    def __init__(self, matcher=None, **kwargs):
        super().__init__(**kwargs)
        self.matcher = matcher
        self._asserted_object = None

    def _run(self, *args, **kwargs):
        self.asserts.check(self._asserted_object, self.matcher)


class TaskResultCheck(AbstractMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.parent.result.current, self.matcher)


class TaskEffectiveResultCheck(AbstractMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.parent.result.effective, self.matcher)


class TestEffectiveResultCheck(AbstractMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.parent.result.effective, self.matcher)


class TestResultCheck(AbstractMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.parent.result.current, self.matcher)


class AbstractExecResultMatchesTask(AbstractMatchesTask):
    @property
    def exec_result(self):
        if not self.context:
            return None
        return self.context.config['exec_result']
