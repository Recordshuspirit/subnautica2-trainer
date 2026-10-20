from __future__ import annotations

import json
from pathlib import Path

from subnautica2_trainer.models.offsets import load_offsets


def test_load_offsets(tmp_path: Path):
    payload = {
        "game_version": "1.0.3.12",
        "oxygen": "0x10",
        "health": "0x14",
        "hunger": "0x18",
        "thirst": "0x1C",
        "inventory_base": "0x1000",
    }
    f = tmp_path / "offsets.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    table = load_offsets(f)
    assert table.oxygen == 0x10
    assert table.inventory_base == 0x1000
    assert table.game_version == "1.0.3.12"