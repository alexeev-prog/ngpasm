from enum import Enum

from ngpasm.mnemonics.base import _BasicMnemonic
from ngpasm.registers import get_registers


class ProgramMode(Enum):
    x16bit = "16"
    x32bit = "32"
    x64bit = "64"


class ASMProgram:
    def __init__(self, filename: str, mode: ProgramMode):
        self.filename = filename
        self.mode = mode
        self._mnemonics = []
        self._current_indent_level = 0
        self._indent = ""
        self._regs = get_registers(self.mode.value)

    @property
    def regs(self):
        return self._regs

    def insert_mnemonic(self, mnemonic: _BasicMnemonic):
        self._mnemonics.append(mnemonic)

    def generate(self):
        program = [mnemonic.construct(self._indent) for mnemonic in self._mnemonics]

        return "\n".join(program)
