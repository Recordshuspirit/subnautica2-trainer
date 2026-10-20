"""High-level memory read/write service with pointer chain resolution."""
from __future__ import annotations

import struct
from dataclasses import dataclass

from ..platform.win32_adapter import Win32Adapter
from .process_service import ProcessService


@dataclass
class PointerChain:
    base_module_offset: int
    offsets: list[int]


class MemoryService:
    def __init__(self, adapter: Win32Adapter, process: ProcessService) -> None:
        self._adapter = adapter
        self._process = process

    def _read_bytes(self, address: int, size: int) -> bytes:
        return self._adapter.read(self._process.handle.handle, address, size)

    def read_float(self, address: int) -> float:
        return struct.unpack("<f", self._read_bytes(address, 4))[0]

    def read_i32(self, address: int) -> int:
        return struct.unpack("<i", self._read_bytes(address, 4))[0]

    def write_float(self, address: int, value: float) -> None:
        raise NotImplementedError("write path uses WriteProcessMemory wrapper")

    def resolve_chain(self, module_base: int, chain: PointerChain) -> int:
        addr = module_base + chain.base_module_offset
        for offset in chain.offsets[:-1]:
            addr = self.read_i32(addr) + offset
        return addr + chain.offsets[-1]