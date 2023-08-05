import junitparser

from ktdk.asserts.checks.general import CheckTask


class AbstractXUnitSuiteCheck(CheckTask):
    @property
    def suite(self) -> junitparser.TestSuite:
        return self.context.config['xunit_suite']


class AbstractXUnitCaseCheck(CheckTask):
    @property
    def case(self) -> junitparser.TestCase:
        return self.context.config['xunit_case']


class XUnitSuiteFailsCheck(AbstractXUnitSuiteCheck):
    CHECK_NAME = 'xunit_fails'

    @property
    def _asserted_object(self):
        return self.suite.failures


class XUnitSuiteErrorsCheck(AbstractXUnitSuiteCheck):
    CHECK_NAME = 'xunit_errors'

    @property
    def _asserted_object(self):
        return self.suite.errors


class XUnitSuiteNokCheck(AbstractXUnitSuiteCheck):
    CHECK_NAME = 'xunit_nok'

    @property
    def _asserted_object(self):
        return self.suite.errors + self.suite.failures


class XUnitCaseCheck(AbstractXUnitCaseCheck):
    CHECK_NAME = 'xunit_case'

    @property
    def _asserted_object(self):
        return self.case.result
