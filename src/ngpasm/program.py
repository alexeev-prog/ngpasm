from enum import Enum

from ngpasm.mnemonics.base import _BasicMnemonic
from ngpasm.registers import get_registers


class ProgramMode(Enum):
    """Program modes."""

    x16bit = "16"
    x32bit = "32"
    x64bit = "64"


class ASMProgram:
    """Assembler program class."""

    def __init__(self, filename: str, mode: ProgramMode):
        """Initialize a program."""
        self.filename = filename
        self.mode = mode
        self._mnemonics = []
        self._current_indent_level = 0
        self._indent = ""
        self._regs = get_registers(self.mode.value)

    @property
    def regs(self):
        """Get assembly registers."""
        return self._regs

    @property
    def mnemonics(self):
        """Get mnemonics."""
        return self._mnemonics

    def insert_mnemonic(self, mnemonic: _BasicMnemonic):
        """Insert mnemonic to the program."""
        self._mnemonics.append(mnemonic)

    def generate(self):
        """Generate program."""
        program = [mnemonic.construct(self._indent) for mnemonic in self._mnemonics]

        return "\n".join(program)
