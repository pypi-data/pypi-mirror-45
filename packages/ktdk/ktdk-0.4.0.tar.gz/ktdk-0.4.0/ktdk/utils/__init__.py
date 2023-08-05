import difflib
import io
import logging
from pathlib import Path
from typing import AnyStr, Dict, Optional, Union

import yaml

from .file_utils import FileUtils, create_dirs, list_to_path
from .flatters import flatten_all_tasks, flatten_tasks, flatten_tests
from .meta_utils import bind_class_var, load_class, make_subclasses_register, subclasses_by_attr
from .naming import normalize_name, unique_name

log = logging.getLogger(__name__)


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


def universal_reader(content: Union[Path, io.RawIOBase, str], raw=True) -> str:
    content = extract_content(content)
    if isinstance(content, Path):
        with content.open('rb') as fd:
            content = fd.read()
    if hasattr(content, 'read'):
        content = content.read()
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


def get_context_diff(expected: AnyStr, provided: AnyStr, keep_ends=True):
    def _split_string(orig):
        if isinstance(orig, str):
            orig = orig.splitlines(keepends=keep_ends)
        return orig

    decoded_prov = try_decode(provided)
    decoded_exp = try_decode(expected)
    if decoded_exp and decoded_prov:
        expected = _split_string(decoded_exp)
        provided = _split_string(decoded_prov)

    return difflib.context_diff(expected, provided, fromfile='expected', tofile='provided')


def extract_content(content: Union[str, dict, bytes]):
    """Extracted content
    Args:
        content: Content input
    Returns:

    """
    if isinstance(content, dict):
        return Path(content.get('file'))
    if isinstance(content, str):
        return io.StringIO(content)
    if isinstance(content, bytes):
        return io.BytesIO(content)
    if isinstance(content, Path):
        return content
    if isinstance(content, io.RawIOBase):
        return content
    return content

