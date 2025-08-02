from ngpasm.mnemonics.base import _ABCBasicMnemonic


class AddMnemonic(_ABCBasicMnemonic):
    """
    The ADD instruction in assembler performs the addition of two operands.

    A mandatory rule is that the operands are equal in size; only two 16-bit numbers
    or two 8-bit numbers can be added to each other.
    """

    def _validate(self) -> None:
        """Validate the mnemonic."""
        if len(self.operands) != 2:
            raise ValueError(
                f"Mnemonic ADD required 2 operands;but get {len(self.operands)}"
            )

    def _generate_default_comment(self) -> str:
        return f"Adding the {self.operands[1]!s} value to the {self.operands[0]!s}"


class SubMnemonic(_ABCBasicMnemonic):
    """
    The ASM sub mnemonic is a subtraction instruction.

    It subtracts the source operand from the destination
    operand and replaces the destination with the result.
    """

    def _validate(self) -> None:
        """Validate the mnemonic."""
        if len(self.operands) != 2:
            raise ValueError(
                f"Mnemonic SUB required 2 operands;but get {len(self.operands)}"
            )

    def _generate_default_comment(self) -> str:
        return f"Substract the {self.operands[1]!s} value to the {self.operands[0]!s}"


class DivMnemonic(_ABCBasicMnemonic):
    """
    The ASM DIV mnemonic is a division instruction.

    It divise the source operand from the destination
    operand and replaces the destination with the result.
    """

    def _validate(self) -> None:
        """Validate the mnemonic."""
        if len(self.operands) != 2:
            raise ValueError(
                f"Mnemonic DIV required 2 operands;but get {len(self.operands)}"
            )

    def _generate_default_comment(self) -> str:
        return f"Divising the {self.operands[1]!s} value to the {self.operands[0]!s}"


class MulMnemonic(_ABCBasicMnemonic):
    """
    The ASM MUL mnemonic is a multiplication instruction.

    It multiplicates the source operand from the destination
    operand and replaces the destination with the result.
    """

    def _validate(self) -> None:
        """Validate the mnemonic."""
        if len(self.operands) != 2:
            raise ValueError(
                f"Mnemonic MUL required 2 operands;but get {len(self.operands)}"
            )

    def _generate_default_comment(self) -> str:
        return (
            f"Multiplicating the {self.operands[1]!s} value to the {self.operands[0]!s}"
        )


class IncMnemonic(_ABCBasicMnemonic):
    """The ASM INC mnemonic is a increment instruction. It increments the register."""

    def _validate(self) -> None:
        """Validate the mnemonic."""
        if len(self.operands) != 1:
            raise ValueError(
                f"Mnemonic INC required 1 operands;but get {len(self.operands)}"
            )

    def _generate_default_comment(self) -> str:
        return f"Increment {self.operands[0]!s}"


class DecMnemonic(_ABCBasicMnemonic):
    """The ASM DEC mnemonic is a decrement instruction. It decrements the register."""

    def _validate(self) -> None:
        """Validate the mnemonic."""
        if len(self.operands) != 1:
            raise ValueError(
                f"Mnemonic DEC required 1 operands;but get {len(self.operands)}"
            )

    def _generate_default_comment(self) -> str:
        return f"Decrement {self.operands[0]!s}"
