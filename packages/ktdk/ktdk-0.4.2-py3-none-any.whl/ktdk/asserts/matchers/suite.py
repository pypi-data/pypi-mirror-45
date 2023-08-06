from ktdk.asserts.matchers.general import GeneralMatcher


class ChecksPassed(GeneralMatcher):
    MATCHER_NAME = 'checks_passed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='checks has passed')
        self.message = self.message or 'Checks did not passed'

    def predicate(self, orig):
        return orig.asserts.passed


class ChecksFailed(GeneralMatcher):
    MATCHER_NAME = 'checks_failed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='checks has failed')
        self.message = self.message or 'Checks did not failed'

    def predicate(self, orig):
        return orig.asserts.failed


class ResultPassed(GeneralMatcher):
    MATCHER_NAME = 'result_passed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='result has passed')
        self.message = self.message or 'Result did not passed'

    def predicate(self, orig):
        return orig.passed


class ResultFailed(GeneralMatcher):
    MATCHER_NAME = 'result_failed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='result has failed')
        self.message = self.message or 'Result did not failed'

    def predicate(self, orig):
        return orig.failed


class CommandOK(GeneralMatcher):
    MATCHER_NAME = 'command_ok'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='Command is OK')
        self.message = self.message or 'Command is not OK'

    def predicate(self, orig):
        return orig.ok


class CommandFailed(GeneralMatcher):
    MATCHER_NAME = 'command_failed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='Command has Failed')
        self.message = self.message or 'Command has not Failed'

    def predicate(self, orig):
        return orig.ok


class StdoutIsEmpty(GeneralMatcher):
    MATCHER_NAME = 'stdout_empty'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='Stdout is not empty')
        self.message = self.message or 'Stdout is not empty'

    def message_footer(self, orig):
        return super().message_footer(orig=orig.stderr.content)

    def predicate(self, orig):
        return orig.stdout.empty


class StdoutIsNotEmpty(GeneralMatcher):
    MATCHER_NAME = 'stdout_not_empty'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='Stdout is empty')
        self.message = self.message or 'Stdout is empty'

    def message_footer(self, orig):
        return super().message_footer(orig=orig.stderr.content)

    def predicate(self, orig):
        return not orig.result.stdout.empty


class StderrIsEmpty(GeneralMatcher):
    MATCHER_NAME = 'stderr_empty'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='Stderr is not empty')
        self.message = self.message or 'Stderr is not empty'

    def message_footer(self, orig):
        return super().message_footer(orig=orig.stderr.content)

    def predicate(self, orig):
        return orig.result.stderr.empty


class StderrIsNotEmpty(GeneralMatcher):
    MATCHER_NAME = 'stderr_not_empty'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='Stderr is empty')
        self.message = self.message or 'Stderr is empty'

    def message_footer(self, orig):
        return super().message_footer(orig=orig.stderr.content)

    def predicate(self, orig):
        return not orig.result.stderr.empty
