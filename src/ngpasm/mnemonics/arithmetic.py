"""
Arithmetic mnemonics module for NGPASM.

This module provides arithmetic assembly instructions including
addition, subtraction, multiplication, division, increment, and decrement.
"""

from typing import ClassVar

from ngpasm.mnemonics.base import (
    BaseMnemonic,
    CommentGenerator,
    OneOperandValidator,
    Operand,
    TwoOperandValidator,
)
from ngpasm.registers import Register


class ArithmeticCommentGenerator(CommentGenerator):
    """
    Specialized comment generator for arithmetic operations.

    This generator creates context-aware comments for arithmetic instructions
    like ADD, SUB, MUL, DIV, INC, and DEC, using appropriate templates
    for each instruction type.

    Attributes:
        _templates: Class variable mapping instruction names to comment templates.
            Templates use {dst} and {src} placeholders for operands.

    """

    _templates: ClassVar[dict[str, str]] = {
        "add": "Adding {src} to {dst}",
        "sub": "Subtracting {src} from {dst}",
        "mul": "Multiplying {dst} by {src}",
        "div": "Dividing {dst} by {src}",
        "inc": "Incrementing {dst}",
        "dec": "Decrementing {dst}",
    }

    def generate(self, mnemonic_name: str, operands: list[Operand]) -> str:
        """
        Generate an arithmetic-specific comment for the instruction.

        Args:
            mnemonic_name: Name of the arithmetic instruction.
            operands: List of operands for the instruction.

        Returns:
            A formatted comment string describing the arithmetic operation.
            Falls back to default comment generation if no template exists.

        """
        template = self._templates.get(mnemonic_name.lower())
        if template:
            if len(operands) == 2:
                return template.format(dst=operands[0], src=operands[1])
            return template.format(dst=operands[0])
        return super().generate(mnemonic_name, operands)


class ArithmeticMnemonic(BaseMnemonic):
    """
    Base class for arithmetic mnemonics with common behavior.

    This class provides a foundation for all arithmetic instructions,
    automatically setting up the appropriate validator based on the
    expected number of operands and using arithmetic-specific comment generation.

    """

    def __init__(
        self,
        name: str,
        expected_operands: int,
        *operands: Register | str | int,
        enable_comment: bool = True,
    ) -> None:
        """
        Initialize an arithmetic mnemonic.

        Args:
            name: The arithmetic instruction name (e.g., 'add', 'sub').
            expected_operands: Number of operands required (1 or 2).
            *operands: Variable number of instruction operands.
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If expected_operands is not 1/2, or if operand count mismatch.

        """
        validator: OneOperandValidator | TwoOperandValidator = (
            TwoOperandValidator(name)
            if expected_operands == 2
            else OneOperandValidator(name)
        )
        comment_generator = ArithmeticCommentGenerator()
        super().__init__(
            name, validator, comment_generator, *operands, enable_comment=enable_comment
        )


class AddMnemonic(ArithmeticMnemonic):
    """
    ADD instruction - adds source to destination.

    This mnemonic performs addition operation: destination = destination + source.
    Requires exactly two operands.

    Example:
        AddMnemonic(Register.EAX, Register.EBX)  ; Adds EBX to EAX

    """

    def __init__(
        self, *operands: Register | str | int, enable_comment: bool = True
    ) -> None:
        """
        Initialize an ADD instruction.

        Args:
            *operands: Two operands (destination, source).
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If not exactly two operands are provided.

        """
        super().__init__("add", 2, *operands, enable_comment=enable_comment)


class SubMnemonic(ArithmeticMnemonic):
    """
    SUB instruction - subtracts source from destination.

    This mnemonic performs subtraction operation: destination = destination - source.
    Requires exactly two operands.

    Example:
        SubMnemonic(Register.EAX, Register.EBX)  ; Subtracts EBX from EAX

    """

    def __init__(
        self, *operands: Register | str | int, enable_comment: bool = True
    ) -> None:
        """
        Initialize a SUB instruction.

        Args:
            *operands: Two operands (destination, source).
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If not exactly two operands are provided.

        """
        super().__init__("sub", 2, *operands, enable_comment=enable_comment)


class MulMnemonic(ArithmeticMnemonic):
    """
    MUL instruction - multiplies destination by source.

    This mnemonic performs multiplication operation: destination = destination * source.
    Requires exactly two operands.

    Example:
        MulMnemonic(Register.EAX, Register.EBX)  ; Multiplies EAX by EBX

    """

    def __init__(
        self, *operands: Register | str | int, enable_comment: bool = True
    ) -> None:
        """
        Initialize a MUL instruction.

        Args:
            *operands: Two operands (destination, source).
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If not exactly two operands are provided.

        """
        super().__init__("mul", 2, *operands, enable_comment=enable_comment)


class DivMnemonic(ArithmeticMnemonic):
    """
    DIV instruction - divides destination by source.

    This mnemonic performs division operation: destination = destination / source.
    Requires exactly two operands.

    Example:
        DivMnemonic(Register.EAX, Register.EBX)  ; Divides EAX by EBX

    """

    def __init__(
        self, *operands: Register | str | int, enable_comment: bool = True
    ) -> None:
        """
        Initialize a DIV instruction.

        Args:
            *operands: Two operands (destination, source).
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If not exactly two operands are provided.

        """
        super().__init__("div", 2, *operands, enable_comment=enable_comment)


class IncMnemonic(ArithmeticMnemonic):
    """
    INC instruction - increments register by 1.

    This mnemonic performs increment operation: operand = operand + 1.
    Requires exactly one operand.

    Example:
        IncMnemonic(Register.EAX)  ; Increments EAX by 1

    """

    def __init__(
        self, *operands: Register | str | int, enable_comment: bool = True
    ) -> None:
        """
        Initialize an INC instruction.

        Args:
            *operands: Single operand to increment.
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If not exactly one operand is provided.

        """
        super().__init__("inc", 1, *operands, enable_comment=enable_comment)


class DecMnemonic(ArithmeticMnemonic):
    """
    DEC instruction - decrements register by 1.

    This mnemonic performs decrement operation: operand = operand - 1.
    Requires exactly one operand.

    Example:
        DecMnemonic(Register.EAX)  ; Decrements EAX by 1

    """

    def __init__(
        self, *operands: Register | str | int, enable_comment: bool = True
    ) -> None:
        """
        Initialize a DEC instruction.

        Args:
            *operands: Single operand to decrement.
            enable_comment: Whether to generate comments in output.

        Raises:
            ValueError: If not exactly one operand is provided.

        """
        super().__init__("dec", 1, *operands, enable_comment=enable_comment)
