from typing import Optional

from ktdk.asserts.checks.general import CheckTask


class StyleResultMatchesCheck(CheckTask):
    CHECK_NAME = 'style_result'

    @property
    def _asserted_object(self) -> Optional[str]:
        if not self.context:
            return None
        return self.context.config['style_result']


class ClangTidyResultMatchesCheck(CheckTask):
    CHECK_NAME = 'tidy_result'

    @property
    def _asserted_object(self) -> Optional[str]:
        if not self.context:
            return None
        return self.context.config['tidy_result']
