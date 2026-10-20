"""Application bootstrap: wire services together and start the trainer loop."""
from __future__ import annotations

import logging
import sys

from .config.settings import load_settings
from .platform.win32_adapter import Win32Adapter
from .services.process_service import ProcessService
from .services.memory_service import MemoryService
from .services.trainer_service import TrainerService
from .handlers.cli_handler import CliHandler


def build_trainer() -> TrainerService:
    settings = load_settings()
    adapter = Win32Adapter()
    proc = ProcessService(adapter, process_name=settings.process_name)
    mem = MemoryService(adapter, proc)
    return TrainerService(settings=settings, memory=mem, process=proc)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    trainer = build_trainer()
    cli = CliHandler(trainer)
    return cli.run(argv if argv is not None else sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())