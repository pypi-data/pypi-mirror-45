import logging

from ktdk.core import errors
from ktdk.utils.basic import BasicObject

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
        return f"{self.message}"


class AssertionsChecks:
    def __init__(self, kill=False):
        self._passed = []
        self._failed = []
        self.__kill = kill

    def to_dict(self):
        return dict(
            passed_count=len(self._passed),
            failed=[str(r) for r in self._failed]
            )

    def __str__(self):
        return str(self.to_dict())

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
        if not condition:
            log.warning(f"[CHK] Failed: {message}")
        self.__add_any(col, obj, message)
        self.__proc_check(condition, message)
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

    def __proc_check(self, condition, message):
        if self.__kill and not condition:
            raise errors.KillCheckError(message=message)

    def abort(self, message: str = None):
        self._add_failed(None, message=f"Task aborted: {message}")


class AssertionMixin:
    def inject_checks(self, checks: AssertionsChecks):
        if not hasattr(self, '_asserts'):
            setattr(self, '_asserts', checks)
        else:
            log.debug(f"Resetting checks: {self.asserts} to {checks}")
            setattr(self, '_asserts', checks)

    @property
    def asserts(self) -> AssertionsChecks:
        return getattr(self, '_asserts', None)
