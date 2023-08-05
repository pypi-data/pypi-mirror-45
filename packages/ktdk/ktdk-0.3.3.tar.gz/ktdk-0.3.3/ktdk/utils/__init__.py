import io
import logging
from pathlib import Path
from typing import AnyStr, Dict, List, Optional, Union

import yaml

from .flatters import flatten_all_tasks, flatten_tasks, flatten_tests
from .naming import normalize_name, unique_name

log = logging.getLogger(__name__)


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


def parse_yaml_config(file_path: Path) -> Optional[Dict]:
    """Loads the YAML file from the defined path
    Args:
        file_path: File path from which the YAML file should be loaded

    Returns(Dictionary): loaded yaml

    """
    file_path = Path(file_path)
    if not file_path.exists():
        log.warning(f"[YAML] Cannot load file - not exists: {file_path}")
        return {}
    with file_path.open('r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            # TODO Throw an exception
            log.error(f"[PARSE] Error for {file_path}: {exc}")
    return {}


def save_yaml(file_path, config):
    """Saves the config to the config file
    Args:
        file_path: YAML file path
        config: Configuration holder

    """
    file_path = Path(file_path)
    with file_path.open('w') as stream:
        try:
            yaml.safe_dump(config, stream, default_flow_style=False)
        except yaml.YAMLError as exc:
            # TODO Throw an exception
            log.error(f"[SAVE] Error: {exc}")


def universal_reader(input: Union['Path', 'io.TextIOBase', 'str'], raw=True) -> str:
    content = input
    if isinstance(input, Path):
        with input.open('rb') as fd:
            content = fd.read()
    if isinstance(input, io.TextIOBase):
        content = input.read()
    if raw:
        return content
    else:
        return content.decode('utf-8')


def dig_class(obj, *selector):
    current = obj
    for sel in selector:
        current = getattr(current, sel)
        if not current:
            return None
    return current


def try_decode(provided: AnyStr) -> Optional[str]:
    if not hasattr(provided, 'decode'):
        return provided
    try:
        return provided.decode('utf-8')
    except UnicodeError:
        return None


def try_encode(provided: AnyStr) -> Optional[str]:
    if not hasattr(provided, 'encode'):
        return provided
    try:
        return provided.encode('utf-8')
    except UnicodeError:
        return None
