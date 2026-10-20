# Contributing to subnautica2-trainer

Thanks for your interest in improving the Subnautica 2 Trainer.

## Reporting offset drift

Game patches frequently shift pointer tables. When a cheat stops working:

1. Run `python -m subnautica2_trainer attach` with logging enabled.
2. Record the new static address with Cheat Engine or a similar scanner.
3. Submit a PR updating `config/offsets.json` and bump `game_version`.

## Code layout

- `src/subnautica2_trainer/platform/` — Win32 adapters (process, memory).
- `src/subnautica2_trainer/services/` — business logic (attach, read, tick).
- `src/subnautica2_trainer/handlers/` — CLI, hotkeys.
- `src/subnautica2_trainer/models/` — offset tables and session state.

Handlers must remain thin; put logic in services.

## Style

- Python 3.11+, `from __future__ import annotations` at the top.
- Type hints on all public functions.
- Run `pytest` before opening a PR.

## Legal

This repository is for educational reverse-engineering practice. Do not
distribute binaries built from this code, and do not use in online modes.