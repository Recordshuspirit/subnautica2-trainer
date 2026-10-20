"""Runtime state models for the trainer session."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AttachState(str, Enum):
    DETACHED = "detached"
    ATTACHED = "attached"
    ERROR = "error"


@dataclass
class SessionState:
    state: AttachState = AttachState.DETACHED
    pid: int | None = None
    active_flags: list[str] = field(default_factory=list)
    last_error: str | None = None

    def mark_attached(self, pid: int) -> None:
        self.state = AttachState.ATTACHED
        self.pid = pid
        self.last_error = None

    def mark_error(self, message: str) -> None:
        self.state = AttachState.ERROR
        self.last_error = message