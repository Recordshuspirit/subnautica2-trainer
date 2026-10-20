"""File logging helpers for debugging attach failures."""
from __future__ import annotations

import logging
from pathlib import Path


def setup_file_logger(name: str, log_path: Path, level: int = logging.DEBUG) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)
    return logger