import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from ktdk import utils
from ktdk.utils.serialization import DumpMixin

log = logging.getLogger(__name__)


class Reporters:
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_INSTANCE'):
            setattr(cls, '_INSTANCE', Reporters())
        return getattr(cls, '_INSTANCE')

    def __init__(self):
        self._reporters = {}
        self.add(Reporter('default'))

    def get(self, name: str) -> 'Reporter':
        return self._reporters.get(name)

    def __getitem__(self, item) -> 'Reporter':
        return self.get(item)

    def add(self, reporter: 'Reporter'):
        log.info(f"[REPORTER] Adding reporter '{reporter.name}': {reporter}")
        self._reporters[reporter.name] = reporter

    def report(self, report, reporters=None) -> bool:
        reporters = reporters or ['default']
        reported = False
        for r_name in reporters:
            reporter = self.get(r_name)
            if reporter:
                reported = reported or reporter.report(report)
        return reported

    def save_all(self, output_dir):
        for reporter in self._reporters.values():
            reporter.write_dump(output_dir)


class Reporter:
    def __init__(self, name: str = None, disabled=False, tags=None, **kwargs):
        self._name = name
        self._reports = []
        self.disabled: bool = disabled
        self.enabled_tags = tags
        self._config = kwargs

    @property
    def name(self) -> str:
        return self._name

    def disabled_for(self, provided: List[str]) -> bool:
        if self.disabled:
            return True
        if not provided or self.enabled_tags is None:
            return False
        prov_set = set(provided)
        enabled_set = set(self.enabled_tags)
        return bool(prov_set.intersection(enabled_set))

    @property
    def reports(self) -> List['Report']:
        return self._reports

    def report(self, report: 'Report'):
        if not self.disabled_for(report.tags):
            log.info(f"[REPORT] Reporting to '{self.name}': {report}")
            self._reports.append(report)
            return True
        return False

    def __str__(self):
        status = "disabled" if self.disabled else "enabled"
        return f'Reporter {self.name} [{status}] - {self.enabled_tags}'

    def write_dump(self, report_path: Path):
        utils.create_dirs(report_path)
        full = report_path / f"{self.name}.json"
        log.info(f"[REPORT] Saving report '{self.name}' to {full}")
        with full.open('w') as fp:
            return utils.dumper(self.reports, stream=fp)


class Report(DumpMixin):
    def __init__(self, message: str = None, content: str = None, tags=None,
                 created_at: datetime = None, namespace='::'):
        self.message = message
        self.content = content
        self.tags = tags
        self.created_at = created_at
        self.namespace = namespace

    def dump(self) -> Dict:
        return dict(
            message=self.message,
            content=self.content,
            tags=self.tags,
            created_at=self.created_at,
            namespace=self.namespace
        )

    def __str__(self):
        return f"{self.namespace} - [{self.created_at}] - {self.message}"
