from .basic import IsEmpty, IsFalse, IsNone, IsNotEmpty, IsTrue, Diff, \
    Contains, NotContains, NotEquals, IsNotNone, Equals, Greater, GreaterEquals, Less, LessEquals,\
    DictHasKey

from .suite import ChecksFailed, ChecksPassed, CommandOK, \
    CommandFailed, ResultPassed, ResultFailed, StderrIsEmpty, StdoutIsEmpty, StderrIsNotEmpty, \
    StdoutIsNotEmpty

from .general import GeneralExpectedMatcher, GeneralMatcher

from .files import FileExists


def get_matcher(name):
    return GeneralMatcher.matchers_register().get(name)
