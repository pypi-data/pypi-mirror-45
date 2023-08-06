import logging
import re
from pathlib import Path
from typing import Dict

from ktdk import utils
from ktdk.asserts.matchers.general import GeneralExpectedMatcher, GeneralMatcher
from ktdk.utils import get_context_diff

log = logging.getLogger(__name__)


class DictHasKey(GeneralExpectedMatcher):
    MATCHER_NAME = 'has_key'

    def __init__(self, expected, *args, **kwargs):
        super().__init__(expected, *args, **kwargs, symbol='has')
        self.message = self.message or f'Dictionary does not contains key: {expected}'

    def predicate(self, orig: Dict):
        return self.expected in orig


class IsTrue(GeneralMatcher):
    MATCHER_NAME = 'is_true'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is')
        self.message = self.message or 'Is not true'

    def predicate(self, orig):
        return orig is True


class IsFalse(GeneralMatcher):
    MATCHER_NAME = 'is_false'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is')
        self.message = self.message or 'Is not false'

    def predicate(self, orig):
        return orig is False


class Equals(GeneralExpectedMatcher):
    MATCHER_NAME = 'equals'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='==')
        self.message = self.message or 'Does not equals'

    def predicate(self, orig):
        return orig == self.expected


class Regex(GeneralExpectedMatcher):
    MATCHER_NAME = ['regex', 'match']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='==')
        self.message = self.message or 'Does match the regex'
        pattern = self.expected.decode('utf-8') if isinstance(self.expected, bytes) else \
            self.expected
        self.comp = re.compile(pattern)

    def predicate(self, orig) -> bool:
        return bool(self.comp.match(orig))


class NotEquals(GeneralExpectedMatcher):
    MATCHER_NAME = 'not_equals'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='!=')
        self.message = self.message or 'Does equals'

    def predicate(self, orig):
        return orig != self.expected


class Greater(GeneralExpectedMatcher):
    MATCHER_NAME = 'greater'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='>')
        self.message = self.message or 'Is not Greater'

    def predicate(self, orig):
        return orig > self.expected


class Less(GeneralExpectedMatcher):
    MATCHER_NAME = 'less'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='<')
        self.message = self.message or 'Is not Less'

    def predicate(self, orig):
        return orig < self.expected


class LessEquals(GeneralExpectedMatcher):
    MATCHER_NAME = 'less_equals'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='<=')
        self.message = self.message or 'Is not less equal'

    def predicate(self, orig):
        return orig <= self.expected


class GreaterEquals(GeneralExpectedMatcher):
    MATCHER_NAME = 'greater_equals'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='>=')
        self.message = self.message or 'Is not greater equal'

    def predicate(self, orig):
        return orig >= self.expected


class IsNone(GeneralMatcher):
    MATCHER_NAME = 'is_none'

    def predicate(self, orig):
        return orig is None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is None')
        self.message = self.message or 'Is not None'


class IsNotNone(GeneralMatcher):
    MATCHER_NAME = 'is_not_none'

    def predicate(self, orig):
        return orig is not None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is not None')
        self.message = self.message or 'Is None'


class Contains(GeneralExpectedMatcher):
    MATCHER_NAME = 'contains'

    def predicate(self, orig):
        return orig in self.expected

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='in')
        self.message = self.message or 'Does not contains'


class NotContains(GeneralExpectedMatcher):
    MATCHER_NAME = 'not_contains'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='not in', message='Does contains')
        self.message = self.message or 'Does contains'

    def predicate(self, orig):
        return orig not in self.expected


class IsNotEmpty(GeneralMatcher):
    MATCHER_NAME = 'not_empty'

    def predicate(self, orig):
        return orig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is not Empty')
        self.message = self.message or 'Is empty'


class IsEmpty(GeneralMatcher):
    MATCHER_NAME = 'empty'

    def predicate(self, orig):
        return not orig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is Empty')
        self.message = self.message or 'Is not empty'


class Diff(GeneralExpectedMatcher):
    MATCHER_NAME = 'diff'

    def __init__(self, *args, out_file=None, keep_ends=True, diff_options=None,
                 symbol='diff', **kwargs):
        super().__init__(*args, symbol=symbol, **kwargs)
        self.message = self.message or 'Diff is not empty - strings are not the same'
        self._diff_opts = diff_options
        self._keep_ends = keep_ends
        self._out_file=out_file

    def invoke(self, orig):
        content = utils.universal_reader(self.expected)
        log.debug(f"[DIFF] Expected: {content}")
        log.debug(f"[DIFF] Provided: {orig}")
        compare = get_context_diff(expected=content, provided=orig, keep_ends=self._keep_ends)
        list_cmp = list(compare)
        cond = not list_cmp
        message = "\n" + ''.join(list_cmp)
        if self._out_file is not None:
            out = Path(self._out_file)
            utils.create_dirs(out)
            out.write_text(message)
        obj = self.get_object(orig)
        return cond, obj, message
