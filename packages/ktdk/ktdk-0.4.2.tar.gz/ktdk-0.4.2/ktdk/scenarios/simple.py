from ktdk.tasks.command import Command

from ktdk.asserts import matchers, checks
from ktdk.scenarios import Scenario
from ktdk.tasks.cpp import ValgrindCommand
from ktdk.tasks.raw.executable import ExecutableTask


def _make_check(stream, out_file=None):
    return matchers.Diff(stream, out_file=out_file) if stream else matchers.IsEmpty()


class InOutFileScenario(Scenario):
    def __init__(self, executable=None, stdin=None, stdout=None, args=None, stderr=None,
                 executor=None, status_code=0, wd_subdir=None, **kwargs):
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        self._code = status_code
        self._args = args or []
        self._executor = executor or Command
        self._executable = executable
        self._wd_subdir = wd_subdir or ''
        super().__init__(**kwargs)

    def _run(self, *args, **kwargs):
        cfg = dict(input=self._stdin)
        cwd = self.context.paths.workspace / self._wd_subdir
        executable = ExecutableTask(self._executable, *self._args, cwd=cwd,
                                    executor=self._executor, command_config=cfg)
        stdout_check = _make_check(self._stdout)
        stderr_check = _make_check(self._stderr)
        executable.check_that(checks.StdOutMatchesCheck(stdout_check))
        executable.check_that(checks.StdErrMatchesCheck(stderr_check))
        executable.check_that(checks.ReturnCodeMatchesCheck(matchers.Equals(self._code)))
        self.root_test.add_task(executable)

        if self._executor == ValgrindCommand:
            executable.check_that(checks.ValgrindPassedCheck())



