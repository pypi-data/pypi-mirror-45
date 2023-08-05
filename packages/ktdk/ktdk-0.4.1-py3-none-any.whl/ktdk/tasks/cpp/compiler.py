import logging

from typing import List

from ktdk.asserts.matchers import IsNotEmpty
from ktdk.tasks.build_task import BuildTask

log = logging.getLogger(__name__)


class RawCompilerTask(BuildTask):
    BASE_PARAMS = ['executable', 'files', 'compiler', 'use_default_options']

    def __init__(self, executable: str = 'bin_out', files: List = None,
                 compiler=None, use_default_options=True, **kwargs):
        super().__init__(**kwargs)
        self.files = files
        self._compiler = compiler
        self.executable = executable
        self._use_default_options = use_default_options
        self.add_tags('compile')

    @property
    def compiler(self):
        if self._compiler is None:
            self._compiler = self.context.config.get('cpp_compiler')
        return self._compiler

    def compile_run(self, ):
        found_files = self._file_utils.glob_files(self.files, source='workspace')
        self.asserts.require(found_files, matcher=IsNotEmpty("No input files to compile!"))
        str_files = [str(file_to_str) for file_to_str in found_files]
        build_dir = self.get_build_dir()
        exec_path = build_dir / self.executable
        if self.compiler_options and self._use_default_options:
            log.debug(f">>>>> [OPT] Compiler options: {self.compiler_options}")
            self.args.extend(self.compiler_options)
        self.args += ['-o', str(exec_path)]
        self.args += str_files
        log.info(f"[COMPILE] Compile [{self.executable}] with args {self.args}")
        self.execute()
        self.process_result(exec_path)

    def _run(self, *args, **kwargs):
        self._cmd = self.compiler
        log.info(f'[BUILD] Compilation for {self.namespace} - {self._cmd}')
        old_dir = self.move_to_dir(self.target)
        self.compile_run()
        self.move_to_dir(old_dir)

    def process_result(self, exec_path):
        self.context.config.add_test('exec', {self.executable: exec_path})

    def get_build_dir(self):
        return self.context.paths.workspace_path('build', create=True)

    @property
    def compiler_options(self):
        return []


class CCompilerTask(RawCompilerTask):
    TOOL_NAME = 'c_raw'

    @property
    def compiler_options(self):
        return self.context.config['c_compiler_flags']

    @property
    def compiler(self):
        if self._compiler is None:
            self._compiler = self.context.config.get('c_compiler')
        return self._compiler


class CPPCompilerTask(RawCompilerTask):
    TOOL_NAME = 'cpp_raw'

    @property
    def compiler(self):
        if self._compiler is None:
            self._compiler = self.context.config.get('cpp_compiler')
        return self._compiler

    @property
    def compiler_options(self):
        return self.context.config['cpp_compiler_flags']
