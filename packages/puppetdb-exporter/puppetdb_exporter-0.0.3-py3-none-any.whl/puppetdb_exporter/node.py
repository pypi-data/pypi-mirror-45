from enum import Enum


class Status(Enum):
    CHANGED = 'changed'
    FAILED = 'failed'
    NOOP = 'noop'
    SKIPPED = 'skipped'
    UNCHANGED = 'unchanged'
    UNREPORTED = 'unreported'


class Node():
    def __init__(self, certname: str, status: Status) -> None:
        self._certname = certname
        self._status = status

    @property
    def certname(self) -> str:
        return self._certname

    @property
    def status(self) -> Status:
        return self._status
