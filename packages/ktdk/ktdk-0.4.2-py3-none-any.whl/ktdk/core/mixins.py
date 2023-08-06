import logging
from datetime import datetime
from typing import Dict, TYPE_CHECKING

from ktdk import utils
from ktdk.core import errors
from ktdk.core.reporters import Report
from ktdk.runtime.context import Context
from ktdk.utils import FileUtils

if TYPE_CHECKING:
    from ktdk.core.tasks import Task

log = logging.getLogger(__name__)


class ContextMixin:
    @property
    def context(self) -> Context:
        ctx = getattr(self, '_context', None)
        if ctx is None:
            raise errors.ContextIsNotInitializedError(self.__class__.__name__)
        return ctx

    @property
    def has_context(self) -> bool:
        return hasattr(self, '_context')

    def inject_context(self, context):
        setattr(self, '_context', context)


class ReportableMixin(ContextMixin):
    def report(self, message: str, content: str = None, tags=None, reporters=None) -> bool:
        if not self.has_context:
            return False

        if tags is None:
            tags = getattr(self, 'tags')

        report = Report(message=message, tags=tags, content=content,
                        namespace=getattr(self, 'namespace'),
                        created_at=datetime.now())
        return self.context.reporters.report(report, reporters=reporters)


class CheckedMixin:
    def check_that(self, task: 'Task', points_multiplier: float = 0.0, after_tasks: bool = False):
        """Adds the check task
        Args:
            after_tasks:
            points_multiplier: If this task fails, how much from the test points should be discarded
            task(Task): Task instance
        """
        from .tasks import TaskType
        if getattr(task, '_type') == TaskType.NORMAL:
            setattr(task, '_type', TaskType.CHECKED)
        setattr(task, '_points_multiplier', points_multiplier)
        if hasattr(self, 'add_after') and after_tasks:
            self.add_after(task)
        else:
            self.add_task(task)
        return self

    def require_that(self, task: 'Task', points_multiplier: float = 0.0, after_tasks: bool = False):
        """Requires a subtask to pass
        Args:
            after_tasks: It should be executed after the tasks execution
            points_multiplier: If this task fails, how much from the test points should be discarded
            task(Task):
        """
        from .tasks import TaskType
        self.check_that(task, points_multiplier=points_multiplier, after_tasks=after_tasks)
        task.type = TaskType.REQUIRED
        return self

    def abort(self, message: str, points_multiplier: float = 0):
        from ktdk.asserts.checks.general import AbortTask
        log.warning(f"[ABORT] Aborted {self.name}: {message}")
        self.require_that(AbortTask(message=message), points_multiplier=points_multiplier)


class FileUtilsMixin:
    @property
    def _file_utils(self) -> FileUtils:
        if not hasattr(self, '__file_utils') and hasattr(self, 'context'):
            setattr(self, '__file_utils', FileUtils(self.context))
        return getattr(self, '__file_utils')


class ToolTaskMixin:
    TOOL_NAME = None

    @classmethod
    def _base_class(cls):
        return ToolTaskMixin

    @classmethod
    def tools_register(cls) -> Dict:
        return utils.make_subclasses_register(cls._base_class(), 'TOOL_NAME')


class ExecutorMixin:
    EXECUTOR = None

    @classmethod
    def exec_register(cls) -> Dict:
        return utils.make_subclasses_register(ExecutorMixin, 'EXECUTOR')
