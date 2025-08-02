"""
Register module for CPU registers representation.

Provides classes for representing CPU registers in different CPU
architectures (16, 32 and 64-bit).
Includes hierarchical relationships between registers and their sub-registers.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator, Mapping


@dataclasses.dataclass
class Register:
    """
    Represents a CPU register with immutable properties.

    Attributes:
        name: Canonical name of the register
        size: Bit size of the register (8, 16, 32, 64)
        aliases: Alternative names for the register
        parent: Parent register for partial registers

    """

    name: str
    size: int
    aliases: frozenset[str] = dataclasses.field(default_factory=frozenset)
    parent: Register | None = None

    def __post_init__(self) -> None:
        """Validate register size."""
        if self.size not in (8, 16, 32, 64):
            raise ValueError(
                f"Invalid register size: {self.size}. Must be 8, 16, 32 or 64 bits."
            )

    def get_full_hierarchy(self) -> list[Register]:
        """Get full hierarchy of registers including this one and all parents."""
        hierarchy = []
        current: Register | None = self
        while current:
            hierarchy.append(current)
            current = current.parent
        return hierarchy

    def __str__(self):
        return self.name


class BaseRegisterSet(Mapping):
    """Base class for register sets providing common functionality."""

    def __init__(self, bitness: int) -> None:
        """Initialize a base registers set."""
        self.bitness: int = bitness
        self._registers: dict[str, Register] = {}
        self._build_register_set()

    def _build_register_set(self) -> None:
        """Construct register hierarchy for the architecture."""
        raise NotImplementedError

    def __getattr__(self, key: str) -> Register:
        """Get register by name."""
        return self.__getitem__(key)

    def __getitem__(self, key: str) -> Register:
        """Get register by name."""
        if key in self._registers:
            return self._registers[key]
        raise KeyError(f"Register '{key}' not found in {self.bitness}-bit mode")

    def __iter__(self) -> Iterator[str]:
        """Iterate over register names."""
        return iter(self._registers.keys())

    def __len__(self) -> int:
        """Number of registers in the set."""
        return len(self._registers)

    def get(self, name: str, default: Register | None = None) -> Register | None:
        """Get register by name with fallback."""
        return self._registers.get(name.upper(), default)

    def contains(self, name: str) -> bool:
        """Check if register exists in the set."""
        return name.upper() in self._registers


class RegisterSet16(BaseRegisterSet):
    """Register set for 16-bit mode."""

    def _build_register_set(self) -> None:
        # 16-bit general purpose
        ax = Register("AX", 16, aliases=frozenset(["AX_ALIAS"]))
        cx = Register("CX", 16)
        dx = Register("DX", 16)
        bx = Register("BX", 16)
        sp = Register("SP", 16)
        bp = Register("BP", 16)
        si = Register("SI", 16)
        di = Register("DI", 16)

        # 8-bit sub-registers
        al = Register("AL", 8, parent=ax)
        ah = Register("AH", 8, parent=ax)
        cl = Register("CL", 8, parent=cx)
        ch = Register("CH", 8, parent=cx)
        dl = Register("DL", 8, parent=dx)
        dh = Register("DH", 8, parent=dx)
        bl = Register("BL", 8, parent=bx)
        bh = Register("BH", 8, parent=bx)

        # Segment registers
        cs = Register("CS", 16)
        ds = Register("DS", 16)
        es = Register("ES", 16)
        ss = Register("SS", 16)

        # Add all registers
        registers = [
            ax,
            cx,
            dx,
            bx,
            sp,
            bp,
            si,
            di,
            al,
            ah,
            cl,
            ch,
            dl,
            dh,
            bl,
            bh,
            cs,
            ds,
            es,
            ss,
        ]

        # Create mapping with aliases
        self._registers = {}
        for reg in registers:
            self._registers[reg.name] = reg
            for alias in reg.aliases:
                self._registers[alias] = reg


class RegisterSet32(BaseRegisterSet):
    """Register set for 32-bit mode."""

    def _build_register_set(self) -> None:
        # 32-bit general purpose
        eax = Register("EAX", 32, aliases=frozenset(["EAX_ALIAS"]))
        ecx = Register("ECX", 32)
        edx = Register("EDX", 32)
        ebx = Register("EBX", 32)
        esp = Register("ESP", 32)
        ebp = Register("EBP", 32)
        esi = Register("ESI", 32)
        edi = Register("EDI", 32)

        # 16-bit sub-registers
        ax = Register("AX", 16, parent=eax)
        cx = Register("CX", 16, parent=ecx)
        dx = Register("DX", 16, parent=edx)
        bx = Register("BX", 16, parent=ebx)
        sp = Register("SP", 16, parent=esp)
        bp = Register("BP", 16, parent=ebp)
        si = Register("SI", 16, parent=esi)
        di = Register("DI", 16, parent=edi)

        # 8-bit sub-registers
        al = Register("AL", 8, parent=ax)
        ah = Register("AH", 8, parent=ax)
        cl = Register("CL", 8, parent=cx)
        ch = Register("CH", 8, parent=cx)
        dl = Register("DL", 8, parent=dx)
        dh = Register("DH", 8, parent=dx)
        bl = Register("BL", 8, parent=bx)
        bh = Register("BH", 8, parent=bx)

        # Segment registers
        cs = Register("CS", 16)
        ds = Register("DS", 16)
        es = Register("ES", 16)
        ss = Register("SS", 16)
        fs = Register("FS", 16)
        gs = Register("GS", 16)

        # Control registers
        cr0 = Register("CR0", 32)
        cr2 = Register("CR2", 32)
        cr3 = Register("CR3", 32)
        cr4 = Register("CR4", 32)

        # Add all registers
        registers = [
            eax,
            ecx,
            edx,
            ebx,
            esp,
            ebp,
            esi,
            edi,
            ax,
            cx,
            dx,
            bx,
            sp,
            bp,
            si,
            di,
            al,
            ah,
            cl,
            ch,
            dl,
            dh,
            bl,
            bh,
            cs,
            ds,
            es,
            ss,
            fs,
            gs,
            cr0,
            cr2,
            cr3,
            cr4,
        ]

        # Create mapping with aliases
        self._registers = {}
        for reg in registers:
            self._registers[reg.name] = reg
            for alias in reg.aliases:
                self._registers[alias] = reg


class RegisterSet64(BaseRegisterSet):
    """Register set for 64-bit mode."""

    def _build_register_set(self) -> None:
        # 64-bit general purpose
        rax = Register("RAX", 64, aliases=frozenset(["RAX_ALIAS"]))
        rcx = Register("RCX", 64)
        rdx = Register("RDX", 64)
        rbx = Register("RBX", 64)
        rsp = Register("RSP", 64)
        rbp = Register("RBP", 64)
        rsi = Register("RSI", 64)
        rdi = Register("RDI", 64)
        r8 = Register("R8", 64)
        r9 = Register("R9", 64)
        r10 = Register("R10", 64)
        r11 = Register("R11", 64)
        r12 = Register("R12", 64)
        r13 = Register("R13", 64)
        r14 = Register("R14", 64)
        r15 = Register("R15", 64)

        # 32-bit sub-registers
        eax = Register("EAX", 32, parent=rax)
        ecx = Register("ECX", 32, parent=rcx)
        edx = Register("EDX", 32, parent=rdx)
        ebx = Register("EBX", 32, parent=rbx)
        esp = Register("ESP", 32, parent=rsp)
        ebp = Register("EBP", 32, parent=rbp)
        esi = Register("ESI", 32, parent=rsi)
        edi = Register("EDI", 32, parent=rdi)
        r8d = Register("R8D", 32, parent=r8)
        r9d = Register("R9D", 32, parent=r9)
        r10d = Register("R10D", 32, parent=r10)
        r11d = Register("R11D", 32, parent=r11)
        r12d = Register("R12D", 32, parent=r12)
        r13d = Register("R13D", 32, parent=r13)
        r14d = Register("R14D", 32, parent=r14)
        r15d = Register("R15D", 32, parent=r15)

        # 16-bit sub-registers
        ax = Register("AX", 16, parent=eax)
        cx = Register("CX", 16, parent=ecx)
        dx = Register("DX", 16, parent=edx)
        bx = Register("BX", 16, parent=ebx)
        sp = Register("SP", 16, parent=esp)
        bp = Register("BP", 16, parent=ebp)
        si = Register("SI", 16, parent=esi)
        di = Register("DI", 16, parent=edi)
        r8w = Register("R8W", 16, parent=r8d)
        r9w = Register("R9W", 16, parent=r9d)
        r10w = Register("R10W", 16, parent=r10d)
        r11w = Register("R11W", 16, parent=r11d)
        r12w = Register("R12W", 16, parent=r12d)
        r13w = Register("R13W", 16, parent=r13d)
        r14w = Register("R14W", 16, parent=r14d)
        r15w = Register("R15W", 16, parent=r15d)

        # 8-bit sub-registers
        al = Register("AL", 8, parent=ax)
        cl = Register("CL", 8, parent=cx)
        dl = Register("DL", 8, parent=dx)
        bl = Register("BL", 8, parent=bx)
        spl = Register("SPL", 8, parent=sp)
        bpl = Register("BPL", 8, parent=bp)
        sil = Register("SIL", 8, parent=si)
        dil = Register("DIL", 8, parent=di)
        r8b = Register("R8B", 8, parent=r8w)
        r9b = Register("R9B", 8, parent=r9w)
        r10b = Register("R10B", 8, parent=r10w)
        r11b = Register("R11B", 8, parent=r11w)
        r12b = Register("R12B", 8, parent=r12w)
        r13b = Register("R13B", 8, parent=r13w)
        r14b = Register("R14B", 8, parent=r14w)
        r15b = Register("R15B", 8, parent=r15w)

        # Segment registers
        cs = Register("CS", 16)
        ds = Register("DS", 16)
        es = Register("ES", 16)
        ss = Register("SS", 16)
        fs = Register("FS", 16)
        gs = Register("GS", 16)

        # Control registers
        cr0 = Register("CR0", 64)
        cr2 = Register("CR2", 64)
        cr3 = Register("CR3", 64)
        cr4 = Register("CR4", 64)
        cr8 = Register("CR8", 64)

        # Add all registers
        registers = [
            rax,
            rcx,
            rdx,
            rbx,
            rsp,
            rbp,
            rsi,
            rdi,
            r8,
            r9,
            r10,
            r11,
            r12,
            r13,
            r14,
            r15,
            eax,
            ecx,
            edx,
            ebx,
            esp,
            ebp,
            esi,
            edi,
            r8d,
            r9d,
            r10d,
            r11d,
            r12d,
            r13d,
            r14d,
            r15d,
            ax,
            cx,
            dx,
            bx,
            sp,
            bp,
            si,
            di,
            r8w,
            r9w,
            r10w,
            r11w,
            r12w,
            r13w,
            r14w,
            r15w,
            al,
            cl,
            dl,
            bl,
            spl,
            bpl,
            sil,
            dil,
            r8b,
            r9b,
            r10b,
            r11b,
            r12b,
            r13b,
            r14b,
            r15b,
            cs,
            ds,
            es,
            ss,
            fs,
            gs,
            cr0,
            cr2,
            cr3,
            cr4,
            cr8,
        ]

        # Create mapping with aliases
        self._registers = {}
        for reg in registers:
            self._registers[reg.name] = reg
            for alias in reg.aliases:
                self._registers[alias] = reg


def get_registers(mode: str) -> BaseRegisterSet | None:
    """
    Retrieve register set for specified architecture mode.

    Args:
        mode: Target architecture mode. Valid values: '16', '32', '64'

    Returns:
        Register set instance or None for invalid mode.

    Examples:
        >>> regs = get_registers("64")
        >>> regs["RAX"].name
        'RAX'
        >>> regs["RAX"].size
        64

    """
    if mode == "16":
        return RegisterSet16(16)
    if mode == "32":
        return RegisterSet32(32)
    if mode == "64":
        return RegisterSet64(64)
    return None
