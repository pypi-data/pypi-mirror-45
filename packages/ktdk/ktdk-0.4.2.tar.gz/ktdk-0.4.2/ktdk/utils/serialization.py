import json
import logging
from datetime import datetime
from json import JSONEncoder
from pathlib import Path
from typing import Dict

import yaml

log = logging.getLogger(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, DumpMixin):
            return o.dump()
        if isinstance(o, set):
            return list(*o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, object):
            return o.__dict__
        return super(CustomJSONEncoder, self).default(o)


def dump_yaml(obj, stream, default_flow_style=False, throws=False, **kwargs):
    try:
        return yaml.safe_dump(obj, stream, default_flow_style=default_flow_style, **kwargs)
    except yaml.YAMLError as exc:
        log.error(f"[DUMP] Error: {exc}")
        if throws:
            raise throws


def dump_json(obj, stream, throws=False, default=None, **kwargs):
    if default is None:
        default = CustomJSONEncoder
    try:
        if stream is None:
            return json.dumps(obj, cls=default, **kwargs)
        return json.dump(obj, fp=stream, cls=default, **kwargs)
    except json.JSONDecodeError as exc:
        log.error(f"[DUMP] Error: {exc}")
        if throws:
            raise throws
    return None


class DumpMixin:
    def dump(self) -> Dict:
        return self.__dict__

    def __str__(self) -> str:
        return str(self.__class__.__name__) + ": " + str(self.dump())

    def __repr__(self) -> str:
        return self.__str__()


DUMPERS = dict(json=dump_json, yaml=dump_yaml)


def dumper(obj, stream=None, out_format='json', **kwargs):
    dump_func = DUMPERS.get(out_format, 'json')
    return dump_func(obj, stream, **kwargs)
