"""Attach/detach lifecycle for the Subnautica 2 game process."""
from __future__ import annotations

import logging
from typing import Optional

from ..platform.win32_adapter import Win32Adapter, ProcessHandle

log = logging.getLogger(__name__)


class ProcessService:
    def __init__(self, adapter: Win32Adapter, process_name: str) -> None:
        self._adapter = adapter
        self._process_name = process_name
        self._handle: Optional[ProcessHandle] = None

    @property
    def attached(self) -> bool:
        return self._handle is not None

    @property
    def handle(self) -> ProcessHandle:
        if self._handle is None:
            raise RuntimeError("Process not attached; call attach() first")
        return self._handle

    def attach(self) -> bool:
        pid = self._adapter.find_process(self._process_name)
        if pid is None:
            log.warning("Process %s not found", self._process_name)
            return False
        self._handle = self._adapter.open(pid)
        log.info("Attached to %s (pid=%d)", self._process_name, pid)
        return True

    def detach(self) -> None:
        if self._handle is not None:
            self._adapter.close(self._handle.handle)
            self._handle = None