"""Versioned offset tables for Subnautica 2 game builds."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class OffsetTable:
    game_version: str
    oxygen: int
    health: int
    hunger: int
    thirst: int
    inventory_base: int


def load_offsets(path: Path) -> OffsetTable:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return OffsetTable(
        game_version=raw["game_version"],
        oxygen=int(raw["oxygen"], 16),
        health=int(raw["health"], 16),
        hunger=int(raw["hunger"], 16),
        thirst=int(raw["thirst"], 16),
        inventory_base=int(raw["inventory_base"], 16),
    )