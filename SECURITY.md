# Security Policy

## Scope

This project performs read-only memory inspection of the single-player
Subnautica 2 client for educational trainer development. It does not
modify network traffic and does not target anti-cheat protected modes.

## Reporting a vulnerability

If you discover a bug that could cause memory corruption, process
crashes, or unintended writes to the game, please open a private
security advisory rather than a public issue.

Include:

- Subnautica 2 build number (`config/offsets.json` -> `game_version`)
- Windows version
- Reproduction steps
- Relevant excerpt from `logs/trainer.log`

We aim to respond within 72 hours.

## Out of scope

- Bypassing anti-cheat or DRM
- Multiplayer exploits
- Distribution of compiled loaders