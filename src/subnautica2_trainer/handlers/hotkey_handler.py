"""Global hotkey listener for toggling trainer flags in-game."""
from __future__ import annotations

import logging
from typing import Callable

log = logging.getLogger(__name__)

DEFAULT_BINDINGS: dict[str, str] = {
    "F1": "infinite_oxygen",
    "F2": "infinite_health",
    "F3": "no_hunger_thirst",
    "F4": "free_crafting",
    "F5": "instant_scan",
}


class HotkeyHandler:
    def __init__(self, toggle: Callable[[str], None]) -> None:
        self._toggle = toggle
        self._bindings = dict(DEFAULT_BINDINGS)

    def bind(self, key: str, flag: str) -> None:
        self._bindings[key.upper()] = flag

    def on_key(self, key: str) -> None:
        flag = self._bindings.get(key.upper())
        if flag is None:
            return
        log.info("hotkey %s -> toggle %s", key, flag)
        self._toggle(flag)