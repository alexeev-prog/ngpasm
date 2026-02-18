from enum import Enum

from ngpasm.mnemonics.base import BaseMnemonic
from ngpasm.registers import BaseRegisterSet, get_registers


class ProgramMode(Enum):
    """Program modes with corresponding bit sizes."""

    BIT_16 = "16"
    BIT_32 = "32"
    BIT_64 = "64"

    @property
    def bit_size(self) -> int:
        """Get bit size as integer."""
        return int(self.value)


class ASMProgram:
    """
    Assembler program class.

    This class represents an assembly program with its mnemonics,
    registers, and generation capabilities.
    """

    def __init__(self, filename: str, mode: ProgramMode) -> None:
        """
        Initialize an assembly program.

        Args:
            filename: Name of the output file
            mode: Program mode (16/32/64 bit)

        """
        self.filename = filename
        self.mode = mode
        self._mnemonics: list[BaseMnemonic] = []
        self._indent_level: int = 0
        self._registers = get_registers(mode.value)

    @property
    def registers(self) -> BaseRegisterSet | None:
        """Get assembly registers for current mode."""
        return self._registers

    @property
    def mnemonics(self) -> list[BaseMnemonic]:
        """Get list of mnemonics in the program."""
        return self._mnemonics.copy()  # Return copy to prevent external modification

    def add_mnemonic(self, mnemonic: BaseMnemonic) -> None:
        """
        Add a mnemonic to the program.

        Args:
            mnemonic: The mnemonic to add

        Raises:
            TypeError: If mnemonic is not a BaseMnemonic instance

        """
        if not isinstance(mnemonic, BaseMnemonic):
            raise TypeError(f"Expected BaseMnemonic, got {type(mnemonic).__name__}")
        self._mnemonics.append(mnemonic)

    def set_indent_level(self, level: int) -> None:
        """Set indentation level for program generation."""
        self._indent_level = max(0, level)

    def generate(self) -> str:
        """
        Generate the assembly program.

        Returns:
            Formatted assembly program as string

        """
        indent = "    " * self._indent_level
        program_lines = [mnemonic.construct(indent) for mnemonic in self._mnemonics]

        return "\n".join(program_lines)

    def clear(self) -> None:
        """Clear all mnemonics from the program."""
        self._mnemonics.clear()
