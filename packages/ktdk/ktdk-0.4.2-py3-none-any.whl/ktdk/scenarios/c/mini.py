import logging
from pathlib import Path
from typing import Collection, List, Set

from ktdk import Task, Test
from ktdk.asserts import checks, matchers
from ktdk.core.mixins import FileUtilsMixin
from ktdk.scenarios import FullScenario, Scenario
from ktdk.scenarios.simple import InOutFileScenario
from ktdk.tasks import cpp, fs
from ktdk.tasks.cpp import ValgrindCommand

log = logging.getLogger(__name__)


class CMiniSingleTaskScenario(FullScenario):
    """Execute just single CMiniTask scenario
    """

    def __init__(self, task_name: str, points=0.1, wd_subdir=None, executor=ValgrindCommand,
                 **kwargs):
        super().__init__(**kwargs)
        self.task_name = task_name
        self.points = points
        self.executor = executor
        self.wd_subdir = wd_subdir

    def checkout_teacher_files(self):
        log.info(f"[CHECKOUT] All teacher files for task {self.task_name}")
        copy = fs.CopyFiles(f"{self.task_name}/**/*.*", source='test_files', relative=True)
        self.add_task(copy)

    def checkout_student_files(self):
        source_file = f"{self.task_name}/source.c"
        self.require_that(fs.ExistFiles(source_file))
        copy = fs.CopyFiles(source_file, source='submission', relative=True)
        self.add_task(copy)

    def file_tasks(self):
        self.checkout_teacher_files()
        self.checkout_student_files()  # Needs to be in this order

    def compile_tasks(self):
        c_compile = cpp.CCompilerTask(executable=self.task_name,
                                      files=f'{self.task_name}/source.c',
                                      use_default_options=True)
        c_compile.require_that(checks.TaskResultCheck(matcher=matchers.ResultPassed()))
        c_compile.require_that(checks.ExecutableExists(executable=self.task_name))
        self.root_test.add_task(c_compile)
        return c_compile

    def run_tasks(self):
        params = dict(points=self.points)
        if self.wd_subdir:
            params['wd_subdir'] = self.wd_subdir

        subtests = CMiniSubtestForTask(self.task_name, **params)
        self.root_test.add_task(subtests)


class CMiniSubtestForTask(Task, FileUtilsMixin):
    def __init__(self, task_name, points=0.1, wd_subdir=None, **kwargs):
        super().__init__(**kwargs)
        self.task_name = task_name
        self.points = points
        self.wd_subdir = wd_subdir

    @property
    def base(self) -> Path:
        return self.context.paths.workspace / self.task_name

    def __build_paths(self, ext: str) -> List['Path']:
        return list(self.base.glob(f'*.{ext}'))

    @property
    def out_paths(self) -> List['Path']:
        return self.__build_paths('out')

    @property
    def in_paths(self) -> List['Path']:
        return self.__build_paths('in')

    @property
    def args_paths(self) -> List['Path']:
        return self.__build_paths('args')

    @property
    def err_paths(self) -> List['Path']:
        return self.__build_paths('err')

    def _run(self, *args, **kwargs):
        names = dict(
            outs=_resolve_names(self.out_paths),
            ins=_resolve_names(self.in_paths),
            errs=_resolve_names(self.err_paths),
            args=_resolve_names(self.args_paths)
        )

        all_names = set().union(*names.values())
        log.info(f"[MINI] All subtests: {all_names}")
        all_tests = [_build_test(name, names) for name in all_names]

        num = len(all_tests)
        for test in all_tests:
            self._run_one(test, num=num)

    def _in_out_test(self, name, points=0.0, stdin=None, stdout=None,
                     args=None, status_code=0, stderr=None, executor=ValgrindCommand):
        """Create instance of the in/out test
        Args:
            name(str): Test name
            points(float): Number of points for the test
            stdin(Path): File with stdin
            stdout(Path): Stdout file
            args(List['str']): List of arguments
            status_code(int): Status code
            stderr(Path): Stdout path
            executor: Executor instance

        Returns:

        """
        test = Test(name=name, desc=f'Subtest name: {name}', points=points)
        in_out_scenario = InOutFileScenario(
            executable=self.task_name, args=args, stdin=stdin, executor=executor,
            stdout=stdout, stderr=stderr, status_code=status_code, wd_subdir=self.wd_subdir)
        test.add_task(in_out_scenario)
        return test

    def _run_one(self, test: dict, num=0):
        def get_path(val):
            return self.base / val if val else None

        params = {key: get_path(value) for key, value in test.items() if key != 'name'}

        points = self.points / num
        if params.get('args') is not None:
            args_path: Path = params['args']
            if args_path.exists():
                args = args_path.read_text('utf-8').split('\n')
                params['args'] = [arg for arg in args if arg]

        test = self._in_out_test(test['name'], points=points, **params)
        self.test.add_test(test)


class CMiniAllTasksScenario(Scenario):
    def __init__(self, points=1, wd_to_mini_dir=False, **kwargs):
        super().__init__(**kwargs)
        self.points = points
        self.wd_to_mini_dir = wd_to_mini_dir

    def list_teacher_directories(self) -> Set[str]:
        return set(self._file_utils.list_type_in_directories(source='test_files',
                                                             predicate=Path.is_dir))

    def list_of_student_impl(self) -> Set['str']:
        files = self._file_utils.glob_files(pattern='*/source.c', source='submission')
        sources = {p.parent.name for p in files}
        return sources

    def _run(self, *args, **kwargs):
        teacher: set = self.list_teacher_directories()
        student: set = self.list_of_student_impl()
        intersection = student.intersection(teacher)
        num_tasks = len(teacher)
        ratio = self.points / float(num_tasks) if num_tasks else 0
        for task_name in intersection:
            test_for_mini_task = Test(name=task_name, desc=f"Test for task: {task_name}")
            task_scenario = CMiniSingleTaskScenario(task_name=task_name, points=ratio,
                                                    wd_subdir=task_name)
            test_for_mini_task.add_task(task_scenario)
            self.root_test.add_test(test_for_mini_task)


def _resolve_names(collection: Collection['Path']) -> Set['str']:
    return {p.resolve().stem for p in collection}


def _intersect_names(first: Set['str'], *sets) -> Set['str']:
    result = first
    for name_set in sets:
        result = result.intersection(name_set)
    return result


def _build_test(name, names):
    test = dict(
        stdout=f"{name}.out" if name in names['outs'] else None,
        stdin=f"{name}.in" if name in names['ins'] else None,
        stderr=f'{name}.err' if name in names['errs'] else None,
        args=f'{name}.args' if name in names['args'] else None,
        name=name,
    )
    return test
