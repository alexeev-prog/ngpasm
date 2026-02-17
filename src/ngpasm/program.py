from enum import Enum

from ngpasm.mnemonics.base import _BasicMnemonic
from ngpasm.registers import BaseRegisterSet, Register, get_registers


class ProgramMode(Enum):
    """Program modes."""

    x16bit = "16"
    x32bit = "32"
    x64bit = "64"


class ASMProgram:
    """Assembler program class."""

    def __init__(self, filename: str, mode: ProgramMode) -> None:
        """Initialize a program."""
        self.filename: str = filename
        self.mode: ProgramMode = mode
        self._mnemonics: list[_BasicMnemonic] = []
        self._current_indent_level: int = 0
        self._indent: str = ""
        self._regs: list[Register] = get_registers(self.mode.value)

    @property
    def regs(self) -> BaseRegisterSet | None:
        """Get assembly registers."""
        return self._regs

    @property
    def mnemonics(self) -> list[_BasicMnemonic]:
        """Get mnemonics."""
        return self._mnemonics

    def insert_mnemonic(self, mnemonic: _BasicMnemonic) -> None:
        """Insert mnemonic to the program."""
        self._mnemonics.append(mnemonic)

    def generate(self) -> str:
        """Generate program."""
        program: list[str] = [
            mnemonic.construct(self._indent) for mnemonic in self._mnemonics
        ]

        return "\n".join(program)
