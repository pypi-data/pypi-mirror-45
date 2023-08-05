from .general import TaskResultCheck, TaskEffectiveResultCheck, \
    TestResultCheck, TestEffectiveResultCheck

from .executable import ReturnCodeMatchesCheck, StdErrMatchesCheck, \
    StdOutMatchesCheck, ValgrindPassedCheck, ExecutableExists


from .junit import XUnitSuiteErrorsCheck, XUnitSuiteFailsCheck, XUnitSuiteNokCheck, XUnitCaseCheck


from .style import ClangTidyResultMatchesCheck, StyleResultMatchesCheck


