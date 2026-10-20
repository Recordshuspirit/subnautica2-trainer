from __future__ import annotations

import struct

from subnautica2_trainer.services.memory_service import MemoryService, PointerChain


class FakeAdapter:
    def __init__(self, mem: dict[int, bytes]) -> None:
        self._mem = mem

    def read(self, handle: int, address: int, size: int) -> bytes:
        return self._mem[address][:size]


class FakeProcess:
    class _H:
        handle = 1

    handle = _H()

    def __init__(self) -> None:
        pass


def test_read_float():
    payload = struct.pack("<f", 42.5)
    adapter = FakeAdapter({0x1000: payload})
    svc = MemoryService(adapter, FakeProcess())
    assert svc.read_float(0x1000) == 42.5


def test_resolve_chain():
    # base=0x1000, offset=0x10 -> addr 0x1010 holds ptr to 0x2000, final offset 0x8
    table = {
        0x1010: struct.pack("<i", 0x2000),
    }
    adapter = FakeAdapter(table)
    svc = MemoryService(adapter, FakeProcess())
    chain = PointerChain(base_module_offset=0x10, offsets=[0x8])
    assert svc.resolve_chain(0x1000, chain) == 0x2008