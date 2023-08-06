import logging
from pathlib import Path

from ktdk import utils
from ktdk.tasks.command import Command

log = logging.getLogger(__name__)


class ValgrindCommand(Command):
    EXECUTOR = 'valgrind'

    def __init__(self, command, args=None, **kwargs):
        """Creates Valgrind command instance
        Args:
            command(str): Command name
            args(list): Command arguments
        """
        super().__init__(command, args=args, **kwargs)
        self._vargs = []

    @property
    def valgrind_log_file(self) -> str:
        """Gets name of the valgrind log file
        Returns(str): Valgrind log file
        """
        name = self.output_file_name(suffix='valgrind.log')
        test_path = utils.list_to_path(self.task.test.namespace_parts)
        path_name: Path = self.context.paths.outputs / test_path / name
        utils.create_dirs(path_name.parent)
        return str(path_name)

    @property
    def valgrind_command(self):
        """Valgrind command with arguments and sets log file
        Returns(list): valgrind command with valgrind arguments
        """
        args = []
        if self.context:
            valgrind_file = self.valgrind_log_file
            args.append(f'--log-file={valgrind_file}')
            args.extend(self.context.config.get('valgrind_args'))
        cmd = ['valgrind', *args, *self._vargs]
        return cmd

    def add_vargs(self, *args):
        """Adds the valgrind arguments
        Args:
            *args: Valgrind arguments
        Returns(ValgrindCommand): Valgrind command instance
        """
        self._vargs.extend(args)
        return self

    @property
    def executable_command(self):
        """Executable command with arguments
        Returns(list): Executable command with arguments list
        """
        return [self.command, *self.args]

    @property
    def full_command(self):
        """Full command list
        Returns(list): Full command with valgrind and executable
        """
        return [*self.valgrind_command, *self.executable_command]

    def process(self, result):
        """Processes the result
        Args:
            result: Command execution result
        Returns: Processes result
        """
        process_result = super().process(result)
        process_result.outputs['valgrind_log'] = self.valgrind_log_file

        self.context.config.set_test('valgrind_log', self.valgrind_log_file)
        return process_result
