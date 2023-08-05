import difflib
from typing import AnyStr

from ktdk import utils


def get_context_diff(expected: AnyStr, provided: AnyStr, keep_ends=True):
    def _split_string(orig):
        if isinstance(orig, str):
            orig = orig.splitlines(keepends=keep_ends)
        return orig

    decoded_prov = utils.try_decode(provided)
    decoded_exp = utils.try_decode(expected)
    if decoded_exp and decoded_prov:
        expected = _split_string(decoded_exp)
        provided = _split_string(decoded_prov)

    return difflib.context_diff(expected, provided, fromfile='expected', tofile='provided')
