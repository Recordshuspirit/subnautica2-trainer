"""Configuration model and loader for the Subnautica 2 trainer."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(os.getenv("APPDATA", ".")) / "Subnautica2Trainer" / "config.json"


@dataclass
class CheatFlags:
    infinite_oxygen: bool = True
    infinite_health: bool = False
    no_hunger_thirst: bool = True
    free_crafting: bool = False
    instant_scan: bool = True


@dataclass
class TrainerSettings:
    process_name: str = "Subnautica2-Win64-Shipping.exe"
    poll_interval_ms: int = 250
    hotkeys_enabled: bool = True
    flags: CheatFlags = field(default_factory=CheatFlags)


def load_settings(path: Path | None = None) -> TrainerSettings:
    cfg_path = path or DEFAULT_CONFIG_PATH
    settings = TrainerSettings()
    if not cfg_path.exists():
        return settings
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    settings.process_name = raw.get("process_name", settings.process_name)
    settings.poll_interval_ms = int(raw.get("poll_interval_ms", settings.poll_interval_ms))
    settings.hotkeys_enabled = bool(raw.get("hotkeys_enabled", settings.hotkeys_enabled))
    flags = raw.get("flags", {})
    for key, value in flags.items():
        if hasattr(settings.flags, key):
            setattr(settings.flags, key, bool(value))
    return settings