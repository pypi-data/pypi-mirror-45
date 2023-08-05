from typing import Dict

from .general import TaskResultCheck, TaskEffectiveResultCheck, \
    TestResultCheck, TestEffectiveResultCheck, CheckTask

from .executable import ReturnCodeMatchesCheck, StdErrMatchesCheck, \
    StdOutMatchesCheck, ValgrindPassedCheck, ExecutableExists


from .junit import XUnitSuiteErrorsCheck, XUnitSuiteFailsCheck, XUnitSuiteNokCheck, XUnitCaseCheck


from .style import ClangTidyResultMatchesCheck, StyleResultMatchesCheck
