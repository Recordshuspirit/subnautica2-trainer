"""Trainer orchestration: dispatches cheat flags to the correct memory offsets."""
from __future__ import annotations

import logging
import time
from typing import Callable

from ..config.settings import TrainerSettings
from .memory_service import MemoryService
from .process_service import ProcessService

log = logging.getLogger(__name__)

# Static offsets are versioned per game patch; keep them in one place.
OFFSET_OXYGEN_PTR = 0x02A15F40
OFFSET_HEALTH_PTR = 0x02A15F48
OFFSET_HUNGER_PTR = 0x02A15F50


class TrainerService:
    def __init__(
        self,
        settings: TrainerSettings,
        memory: MemoryService,
        process: ProcessService,
    ) -> None:
        self.settings = settings
        self._memory = memory
        self._process = process
        self._running = False
        self._tick_handlers: dict[str, Callable[[], None]] = {
            "infinite_oxygen": self._tick_oxygen,
            "infinite_health": self._tick_health,
            "no_hunger_thirst": self._tick_hunger,
        }

    def attach(self) -> bool:
        return self._process.attach()

    def _tick_oxygen(self) -> None:
        try:
            self._memory.read_float(OFFSET_OXYGEN_PTR)
        except OSError:
            log.debug("oxygen read failed")

    def _tick_health(self) -> None:
        try:
            self._memory.read_float(OFFSET_HEALTH_PTR)
        except OSError:
            log.debug("health read failed")

    def _tick_hunger(self) -> None:
        try:
            self._memory.read_float(OFFSET_HUNGER_PTR)
        except OSError:
            log.debug("hunger read failed")

    def tick(self) -> None:
        for name, handler in self._tick_handlers.items():
            if getattr(self.settings.flags, name, False):
                handler()

    def run_loop(self) -> None:
        self._running = True
        interval = self.settings.poll_interval_ms / 1000.0
        while self._running:
            if not self._process.attached and not self.attach():
                time.sleep(1.0)
                continue
            self.tick()
            time.sleep(interval)

    def stop(self) -> None:
        self._running = False