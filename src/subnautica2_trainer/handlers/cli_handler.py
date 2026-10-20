"""Thin CLI handler that forwards commands to the trainer service."""
from __future__ import annotations

import argparse

from ..services.trainer_service import TrainerService


class CliHandler:
    def __init__(self, trainer: TrainerService) -> None:
        self._trainer = trainer

    def _build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="subnautica2-trainer")
        sub = parser.add_subparsers(dest="cmd", required=True)
        sub.add_parser("attach", help="attach to Subnautica 2 process")
        enable = sub.add_parser("enable", help="enable a cheat flag")
        enable.add_argument("flag")
        disable = sub.add_parser("disable", help="disable a cheat flag")
        disable.add_argument("flag")
        sub.add_parser("run", help="run the trainer loop")
        return parser

    def run(self, argv: list[str]) -> int:
        args = self._build_parser().parse_args(argv)
        if args.cmd == "attach":
            return 0 if self._trainer.attach() else 1
        if args.cmd == "enable":
            setattr(self._trainer.settings.flags, args.flag, True)
            return 0
        if args.cmd == "disable":
            setattr(self._trainer.settings.flags, args.flag, False)
            return 0
        if args.cmd == "run":
            self._trainer.run_loop()
            return 0
        return 2