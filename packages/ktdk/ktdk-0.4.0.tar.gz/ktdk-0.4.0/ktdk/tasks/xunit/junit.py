import logging
from typing import Union
from xml.etree import ElementTree

from junitparser import JUnitXml, TestCase, TestSuite

from ktdk.asserts.checks.general import TaskResultCheck
from ktdk.asserts.matchers import IsNone, ResultPassed
from ktdk.core.tasks import Task
from ktdk.core.tests import Test

log = logging.getLogger(__name__)


class JUnitParseTask(Task):
    def __init__(self, junit_file=None, **kwargs):
        super().__init__(**kwargs)
        self._junit_file = junit_file
        self._root = None

    @property
    def xml_root(self):
        if self._root is None:
            self._root = JUnitXml.fromfile(str(self._junit_file))
        return self._root

    def parse_xunit(self):
        for suite in self.xml_root:
            log.debug(f"[HANDLE] SUITE: {suite}")
            self.process_the_suite(suite)

    def process_the_suite(self, suite):
        log.debug(f"[JUNIT] Test Suite {suite.name}: {suite}")
        self.context.config.set_test('xunit_suite', suite)
        suite_test = create_test(suite, test=self.test)
        suite_test.add_tags('junit_suite')
        for case in suite:
            _handle_case(case, suite_test=suite_test)
        return suite_test

    def _run(self, *args, **kwargs):
        log.debug(f"[JUNIT] Parse: {self.test.namespace}")
        try:
            return self.parse_xunit()
        except ElementTree.ParseError as ex:
            self.asserts.abort(f"There is an error the JUnit parsing: {ex}")


class _ProcessTestCaseTask(Task):
    def __init__(self, case: TestCase, **kwargs):
        super().__init__(**kwargs)
        self.case = case

    def _run(self, *args, **kwargs):
        self.asserts.check(self.case.result, matcher=IsNone())
        self.context.config.add_test('xunit_case', self.case)


def _handle_case(test_case: TestCase, suite_test: Test):
    log.debug(f"[JUNIT] Test Case {test_case.name} [{test_case.result}]: {test_case}")
    case_test = build_test_case(test_case=test_case)
    suite_test.add_test(case_test)
    return suite_test


def create_test(test_case: Union[TestCase, TestSuite], test: Test = None):
    test = Test() if test is None else test
    test.description = test_case.name or 'Undefined name'
    test.name = test_case.name or 'Undefined name'
    log.debug(f"[JUNIT] Create test: {test_case}")
    return test


def build_test_case(test_case: TestCase):
    test = create_test(test_case=test_case)
    test.add_tags('junit_case')
    process_task = _ProcessTestCaseTask(test_case)
    process_task.check_that(TaskResultCheck(matcher=ResultPassed()))
    test.add_task(process_task)
    return test
