"""Small helpers for inspecting memory regions during offset hunting."""
from __future__ import annotations


def hexdump(data: bytes, width: int = 16) -> str:
    lines: list[str] = []
    for i in range(0, len(data), width):
        chunk = data[i : i + width]
        hex_part = " ".join(f"{b:02X}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{i:08X}  {hex_part:<{width * 3}}  {ascii_part}")
    return "\n".join(lines)


def align(value: int, alignment: int = 0x1000) -> int:
    return (value + alignment - 1) & ~(alignment - 1)