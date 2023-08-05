import logging
import os
import shutil
from pathlib import Path
from typing import Dict, List

from ktdk.asserts.matchers import IsNotEmpty, IsNotNone
from ktdk.core.mixins import FileUtilsMixin, ToolTaskMixin
from ktdk.core.tasks import Task

log = logging.getLogger(__name__)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        source = os.path.join(src, item)
        destination = os.path.join(dst, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination, symlinks, ignore)
        else:
            shutil.copy2(source, destination)


class FileActionWrapper:
    def __init__(self, action, path):
        self.action = action
        self.path = path

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__dict__


class AbstractFilesTask(Task, FileUtilsMixin, ToolTaskMixin):
    @classmethod
    def _base_class(cls):
        return ToolTaskMixin

    def __init__(self, pattern='', subdir='', from_dir=None, to_dir=None, output_subdir=None,
                 source='submission', destination='workspace', overwrite=True, relative=True,
                 **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.destination = destination
        self.subdir = subdir or ''
        self.output_subdir = output_subdir or ''
        self._from_dir = Path(from_dir) if from_dir is not None else None
        self._to_dir = Path(to_dir) if to_dir is not None else None
        self.pattern = [pattern] if isinstance(pattern, str) else pattern
        self.overwrite = overwrite
        self.relative = relative

    @property
    def from_path(self) -> Path:
        if self._from_dir is not None:
            return self._from_dir
        return self.context.paths.get_dir(self.source) / self.subdir

    @property
    def to_path(self):
        if self._to_dir is not None:
            return self._from_dir
        return self.context.paths.get_dir(self.destination) / self.subdir / self.output_subdir

    def _glob_dirs(self, path=None) -> List:
        path = path or self.from_path
        found = []
        if self.pattern:
            for pat in self.pattern:
                found += path.glob(pat)
            return found
        return [path]

    @property
    def bound_params(self) -> Dict:
        return dict(pattern=self.pattern, source=self.source, target=self.destination,
                    subdir=self.subdir, subdir_source=self._from_dir, relative=self.relative,
                    subdir_target=self._to_dir, overwrite=self.overwrite)

    @property
    def bind_glob(self) -> Dict:
        return dict(pattern=self.pattern, source=self.source, subdir=self.subdir)


class CopyFiles(AbstractFilesTask):
    TOOL_NAME = 'copy'

    def _run(self, *args, **kwargs):
        log.info(f"[FS] Copy files {self.namespace}: {self.pattern}")
        self._file_utils.process_files(**self.bound_params, action=shutil.copy2)


class CopyDir(AbstractFilesTask):
    TOOL_NAME = 'copy_dir'

    def _run(self, *args, **kwargs):
        log.info(f"[FS] Copy dir {self.namespace}: {self.pattern}")
        self._file_utils.process_files(**self.bound_params, action=shutil.copytree)


class MoveFiles(AbstractFilesTask):
    TOOL_NAME = 'move'

    def _run(self, *args, **kwargs):
        log.info(f"[FS] Move files {self.namespace}: {self.pattern}")
        self._file_utils.process_files(**self.bound_params, action=shutil.move)


class DeleteFiles(AbstractFilesTask):
    TOOL_NAME = 'delete'

    def _run(self, *args, **kwargs):
        log.info(f"[FS] Delete files {self.namespace}: {self.pattern}")
        files = self._file_utils.glob_files(**self.bind_glob)
        for file_to_delete in files:
            log.debug(f"[DEL] Deleting file: {file_to_delete}")
            file_to_delete.unlink()


class ExistFiles(AbstractFilesTask):
    TOOL_NAME = ['exist', 'exists']

    def _run(self, *args, **kwargs):
        files = self._file_utils.glob_files(**self.bind_glob)
        log.info(f"[FS] Exists files {self.namespace}: {self.pattern}")
        self.asserts.check(
            files,
            IsNotEmpty(message=f'Files not found! Pattern {self.pattern} in {self.from_path}')
        )


class FindFiles(AbstractFilesTask):
    TOOL_NAME = 'find'

    def _run(self, *args, **kwargs):
        files = self._file_utils.glob_files(**self.bind_glob)
        log.debug(f"[FND] Found files with pattern={self.pattern}: {files}")
        self.context.config.add_task('found_files', files)
        self.asserts.check(files, IsNotNone(message=f"Cannot find any files: {self.pattern}"))


class MakeDir(AbstractFilesTask):
    TOOL_NAME = 'mkdir'

    def _run(self, *args, **kwargs):
        log.debug(f"[DIR] Create: {self.from_path}")
        self.from_path.mkdir(parents=True, exist_ok=True)
