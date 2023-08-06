import logging

from ktdk.core import errors
from ktdk.utils.basic import BasicObject
from ktdk.utils.serialization import DumpMixin

log = logging.getLogger(__name__)


class AssertionResult(BasicObject):
    """Defines assertion result object
    """

    def __init__(self, obj=None, message=None, **kwargs):
        super().__init__()
        self.message = message
        self.obj = obj
        self.other = kwargs

    def __str__(self):
        return str(self.message)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.message}"


class AssertionsChecks(DumpMixin):
    def __init__(self, kill=False, task=None):
        self._passed = []
        self._failed = []
        self.__kill = kill
        self._task = task

    def report(self, *args, **kwargs):
        if self._task:
            return self._task.report(*args, **kwargs)
        return None

    def dump(self):
        return dict(
            passed_count=len(self._passed),
            failed=[str(r) for r in self._failed]
        )

    def __add_any(self, what, obj=None, message=None, **kwargs):
        col = getattr(self, what)
        col.append(AssertionResult(obj=obj, message=message, **kwargs))

    def _add_passed(self, obj=None, message=None, **kwargs):
        self.__add_any('_passed', obj=obj, message=message, **kwargs)

    def _add_failed(self, obj=None, message=None, **kwargs):
        self.__add_any('_failed', obj, message, **kwargs)

    def check(self, obj, matcher=None):
        cond, _ = self.__check(obj, matcher=matcher)
        return cond

    def require(self, obj, matcher=None):
        cond, message = self.__check(obj, matcher=matcher)
        if not cond:
            raise errors.RequireFailedError(message)
        return cond

    def __check(self, obj, matcher):
        matcher = matcher or (lambda x: (x, x, x))
        condition, obj, message = matcher(obj)
        col = '_passed' if condition else '_failed'
        self.__add_any(col, obj, message)
        self.__proc_check(condition, message, matcher)
        return condition, message

    @property
    def passed_results(self):
        return self._passed

    @property
    def failed_results(self):
        return self._failed

    @property
    def passed(self):
        return not self._failed

    @property
    def failed(self):
        return not self.passed

    @property
    def _is_checked(self):
        if self._task is None:
            return False
        return self._task.checked

    def __proc_check(self, condition, message, matcher):
        if not condition:
            log.warning(f"[CHK] Failed: {message}")
            if self._is_checked:
                self.report(message=f"Check failed for {matcher.__class__.__name__}",
                            content=message)
        if self.__kill and not condition and self._is_checked:
            raise errors.KillCheckError(message=message)

    def abort(self, message: str = None):
        self._add_failed(None, message=f"Task aborted: {message}")


class AssertionMixin(DumpMixin):
    def inject_checks(self, ins_check: AssertionsChecks):
        if not hasattr(self, '_asserts'):
            setattr(self, '_asserts', ins_check)
        else:
            log.debug(f"Resetting checks: {self.asserts} to {ins_check}")
            setattr(self, '_asserts', ins_check)

    @property
    def asserts(self) -> AssertionsChecks:
        return getattr(self, '_asserts', None)
