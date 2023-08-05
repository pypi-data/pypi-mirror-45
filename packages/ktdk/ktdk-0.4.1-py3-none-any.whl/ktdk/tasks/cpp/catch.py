import logging

from ktdk import Task, Test
from ktdk.asserts import checks, matchers
from ktdk.asserts.checks import ReturnCodeMatchesCheck, StdErrMatchesCheck, \
    ValgrindPassedCheck
from ktdk.asserts.matchers import Equals, IsEmpty
from ktdk.tasks.command import Command
from ktdk.tasks.cpp.valgrind import ValgrindCommand
from ktdk.tasks.raw.executable import ExecutableTask
from ktdk.tasks.xunit import junit
from ktdk.utils import flatters, naming

log = logging.getLogger(__name__)


class CatchRunTestsOneByOneTask(Task):
    BASE_PARAMS = ['executable', 'executor', 'test_args']

    def __init__(self, executable=None, executor=Command, test_args=None, applied_check=None,
                 **kwargs):
        super().__init__(**kwargs)
        self._executable = executable
        self.executor = executor
        self.applied_check = applied_check
        self._test_args = test_args or []

    @property
    def executable(self):
        return self._executable

    @property
    def command_path(self):
        return self.context.config['exec'][self.executable]

    # https://github.com/catchorg/Catch2/blob/master/docs/command-line.md
    def get_the_tests_list(self):
        result = self.run_only_command(self.command_path, '--list-test-names-only',
                                       executor=Command)
        stdout = result.stdout.content
        return stdout.splitlines()

    def run_one_test_by_name(self, test_name):
        test = Test(name=test_name, desc=test_name)
        args = [*self._test_args, '-r', 'junit', '-n', naming.slugify(test_name), test_name]
        exec_task = ExecutableTask(executable=self.executable, args=args, executor=self.executor)
        exec_task.add_post_action(_process_junit_test_run)
        test.add_task(exec_task)
        if self.test is not None:
            self.test.add_test(test)  # Add the newly created test to the test
        return exec_task

    def _run(self, *args, **kwargs):
        tests = self.get_the_tests_list()
        for test_name in tests:
            log.debug(f"[CATCH_RUN] Catch run the test: {test_name}")
            task = self.run_one_test_by_name(test_name=test_name)
            self.check_test_result(task, task.test)

    def run_only_command(self, binary, *params, executor=Command):
        cmd = executor(binary, args=params)
        cmd.set_task(self)
        return cmd.invoke()

    def check_test_result(self, task: Task, test=None):
        test = self.test

        def __default_check(task, test, executor=None):
            task.check_that(ReturnCodeMatchesCheck(matcher=Equals(0)))
            task.check_that(StdErrMatchesCheck(matcher=IsEmpty()))
            if executor == ValgrindCommand:
                task.check_that(ValgrindPassedCheck())

        if self.applied_check is not None:
            return self.applied_check(task, test, self.executor)

        return __default_check(task=task, test=test, executor=self.executor)


def _process_junit_test_run(task: Task):
    log.debug(f"[PROC_JUNIT] JUNIT process: {task.test.namespace} ")
    exec_result = task.context.config['exec_result']
    stdout_path = exec_result.stdout.path
    log.debug(f"[JUNIT] XML Report location: {stdout_path}")
    if stdout_path:
        task.add_task(junit.JUnitParseTask(junit_file=stdout_path))


class CatchCheckAndComputePoint(Task):
    BASE_PARAMS = ['max_points']

    def __init__(self, max_points: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self._max_points = max_points

    def _run(self, *args, **kwargs):
        tests = flatters.flatten_tests(self.test, include_self=False)
        num_tests = len(tests)
        pts_per_test = self._max_points / num_tests
        log.debug(f"[POINTS] Computing points: {self._max_points}/{num_tests} = {pts_per_test}")
        if num_tests == 0:
            self.test.check_that(checks.ValgrindPassedCheck())
            self.test.abort("Tests execution failed - most probably due to the SIGSEGV",
                            points_multipler=0)
            return
        for test in tests:
            test.points = pts_per_test
            test.check_that(checks.XUnitSuiteErrorsCheck(matcher=matchers.Equals(0)))
            test.check_that(checks.XUnitSuiteFailsCheck(matcher=matchers.Equals(0)))
            test.check_that(checks.ValgrindPassedCheck())


class CatchCheckCasesAndComputePoint(Task):
    BASE_PARAMS = ['max_points']

    def __init__(self, max_points=1.0, **kwargs):
        super().__init__(**kwargs)
        self.max_points = max_points

    def _run(self, *args, **kwargs):
        tests = flatters.flatten_tests(self.test, include_self=False)
        tests = [test for test in tests if 'junit_case' in test.tags]
        num_tests = len(tests)
        pts_per_test = self.max_points / num_tests if num_tests else 0
        log.debug(f"[POINTS] Computing points: {self.max_points}/{num_tests} = {pts_per_test}")
        for test in tests:
            test.points = pts_per_test
            test.check_that(checks.XUnitCaseCheck(matcher=matchers.Equals(0)))
            test.check_that(checks.ValgrindPassedCheck())
