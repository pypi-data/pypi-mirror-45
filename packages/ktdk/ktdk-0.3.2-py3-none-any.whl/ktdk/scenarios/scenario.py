import logging

from ktdk import KTDK, Task, Test
from ktdk.tasks import fs

log = logging.getLogger(__name__)


class Scenario(Task):
    @property
    def ktdk(self) -> KTDK:
        return KTDK.instance

    @property
    def root_test(self) -> Test:
        return self.test

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FullScenario(Scenario):
    @property
    def ft(self):
        ft = fs.FileTasks()
        self.root_test.add_task(ft)
        return ft

    def file_tasks(self):
        pass

    def compile_tasks(self):
        pass

    def run_tasks(self):
        pass

    def evaluate_tasks(self):
        pass

    def _run(self, *args, **kwargs):
        log.info(f"[SCENARIO] Execute scenario {self.namespace}")
        self.file_tasks()
        self.compile_tasks()
        self.run_tasks()
        self.evaluate_tasks()
