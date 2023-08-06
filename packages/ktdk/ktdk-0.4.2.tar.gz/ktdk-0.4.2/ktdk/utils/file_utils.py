import logging
from pathlib import Path

from typing import List

log = logging.getLogger(__name__)


class FileUtils:
    def __init__(self, context):
        self.context = context

    def _build_dir(self, source='workspace', subdir='', path=None) -> Path:
        if path:
            return Path(path)
        result = self.context.paths.get_dir(source)
        subdir = subdir if isinstance(subdir, list) else [subdir]
        return result / list_to_path(subdir)

    def glob_files(self, pattern, source='workspace', subdir='', path=None) -> List[Path]:
        location_dir: Path = self._build_dir(source=source, subdir=subdir, path=path)
        result = []
        if isinstance(pattern, str):
            pattern = [pattern]
        for item in pattern:
            result += location_dir.glob(item)
        log.debug(f"[GLOB] For pattern {pattern} in {location_dir} found: {result}")
        return result

    def list_directory_content(self, source='workspace', subdir='', path=None) -> List['str']:
        location_dir: Path = self._build_dir(source=source, subdir=subdir, path=path)
        import os
        return [dI for dI in os.listdir(str(location_dir))]

    def list_type_in_directories(self, source='workspace', subdir='', path=None, predicate=None):
        location_dir: Path = self._build_dir(source=source, subdir=subdir, path=path)
        content = self.list_directory_content(source=source, subdir=subdir, path=path)
        if predicate is None:
            return content
        return [c for c in content if predicate(location_dir.joinpath(c))]

    def exist_files(self, pattern, where='workspace', subdir='') -> bool:
        return len(self.glob_files(pattern=pattern, source=where, subdir=subdir)) >= 1

    def process_files(self, pattern, source='submission', target='workspace', action=None,
                      overwrite=True, subdir='', subdir_source='', subdir_target='',
                      transform=None, relative=True, **kwargs):
        subdir_target = Path(subdir or '') / (subdir_target or '')
        subdir_source = Path(subdir or '') / (subdir_source or '')
        location_dir: Path = self._build_dir(source=source, subdir=subdir)
        found = self.glob_files(pattern, source=source, subdir=subdir_source)
        paths = transform_path(found, transform)
        for found_file in paths:
            base_dir = location_dir if relative else None
            output_path = self.output_file(file_path=found_file, base_dir=base_dir,
                                           target=target, subdir_target=subdir_target)
            log.debug(f"[PROC] Manipulation ({action.__name__}): "
                      f"{found_file} -> {output_path}")
            create_dirs(output_path.parent)
            if not overwrite and output_path.exists():
                log.debug(f"[SKIP] File already exist: {output_path}")
            else:
                action(found_file, output_path, **kwargs)

    def output_file(self, file_path, target='workspace', subdir_target='', base_dir=None):
        file_path = Path(file_path)
        sub_path = file_path.name
        if base_dir:
            sub_path = file_path.relative_to(base_dir)
        output_dir = self._build_dir(source=target, subdir=subdir_target)
        return output_dir / sub_path


def transform_path(paths, action=None):
    action = action or (lambda x: x)
    return [action(p) for p in paths]


def create_dirs(path: Path, parent=False):
    if parent:
        path = path.parent
    if not path.exists():
        log.debug(f"[DIR] Dir not exists, creating: {path.parent}")
        path.mkdir(parents=True)


def list_to_path(parts: List['str']) -> Path:
    path = Path()
    for pth in parts:
        path /= pth
    return path


def out_test_path(test, file_name):
    path = list_to_path(test.namespace_parts) if test else Path()
    return path / file_name


def out_task_path(task, file_name):
    fn = task.task_namespace + "-" + file_name
    if len(fn) > 255:
        fn = file_name
    return fn
