"""Win32 platform adapter: process enumeration and ReadProcessMemory wrappers."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass

PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260),
    ]


@dataclass
class ProcessHandle:
    pid: int
    handle: int


class Win32Adapter:
    def __init__(self) -> None:
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    def find_process(self, exe_name: str) -> int | None:
        snapshot = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot == -1:
            return None
        entry = PROCESSENTRY32()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
        try:
            ok = self.kernel32.Process32First(snapshot, ctypes.byref(entry))
            while ok:
                if entry.szExeFile.decode(errors="ignore").lower() == exe_name.lower():
                    return int(entry.th32ProcessID)
                ok = self.kernel32.Process32Next(snapshot, ctypes.byref(entry))
        finally:
            self.kernel32.CloseHandle(snapshot)
        return None

    def open(self, pid: int) -> ProcessHandle:
        handle = self.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not handle:
            raise OSError(f"OpenProcess failed for pid {pid}: {ctypes.get_last_error()}")
        return ProcessHandle(pid=pid, handle=handle)

    def read(self, handle: int, address: int, size: int) -> bytes:
        buf = ctypes.create_string_buffer(size)
        read = ctypes.c_size_t(0)
        ok = self.kernel32.ReadProcessMemory(
            handle, ctypes.c_void_p(address), buf, size, ctypes.byref(read)
        )
        if not ok:
            raise OSError(f"ReadProcessMemory failed at 0x{address:X}")
        return buf.raw[: read.value]

    def close(self, handle: int) -> None:
        self.kernel32.CloseHandle(handle)