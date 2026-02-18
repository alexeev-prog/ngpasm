"""
Base classes and utilities for assembly mnemonics.

This module provides the foundation for creating assembly language mnemonics
with support for operand validation, comment generation, and instruction formatting.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ngpasm.registers import Register


@dataclass
class Operand:
    """
    Represents a mnemonic operand.

    This class wraps an operand value to provide consistent string representation
    and type handling across different operand types.

    Attributes:
        value: The actual operand value which can be a Register, string, or integer.

    """

    value: Register | str | int

    def __str__(self) -> str:
        """
        Convert operand to string representation.

        Returns:
            String representation of the operand value.

        """
        return str(self.value)


class OperandValidator(ABC):
    """Base class for operand validation strategies."""

    @abstractmethod
    def validate(self, operands: list[Operand]) -> None:
        """
        Validate operands for a specific instruction type.

        Args:
            operands: List of operands to validate.

        Raises:
            ValueError: If operands fail validation criteria.

        """


class CommentGenerator(ABC):
    """Base class for comment generation strategies."""

    @abstractmethod
    def generate(self, mnemonic_name: str, operands: list[Operand]) -> str:
        """
        Generate a comment for an instruction.

        Args:
            mnemonic_name: Name of the mnemonic/instruction.
            operands: List of operands used with the instruction.

        Returns:
            Generated comment string.

        """


class DefaultCommentGenerator(CommentGenerator):
    """Default comment generation strategy."""

    def generate(self, mnemonic_name: str, operands: list[Operand]) -> str:
        """
        Generate default comment based on operand count.

        Args:
            mnemonic_name: Name of the mnemonic/instruction.
            operands: List of operands used with the instruction.

        Returns:
            Context-sensitive default comment string.

        """
        operand_count: int = len(operands)
        instruction: str = mnemonic_name.upper()

        if operand_count == 0:
            return f"{instruction} operation."
        if operand_count == 1:
            return f"{instruction} operand {operands[0]}."
        if operand_count == 2:
            return f"{instruction} from {operands[1]} to {operands[0]}."
        return f"{instruction} with {operand_count} operands."


class BaseMnemonic:
    """
    Base class for assembly mnemonics following SOLID principles.

    This class provides core functionality for constructing assembly instructions
    with flexible operand handling, validation strategies, and comment generation.

    Attributes:
        name: Assembly instruction name (e.g., 'mov', 'add').
        operands: List of instruction operands wrapped as Operand objects.
        validator: Strategy for operand validation.
        comment_generator: Strategy for comment generation.
        enable_comment: Flag to control comment generation.
        custom_comment: Custom comment override.

    """

    def __init__(
        self,
        name: str,
        validator: OperandValidator,
        comment_generator: CommentGenerator = None,
        *operands: Register | str | int,
        enable_comment: bool = True,
    ) -> None:
        """
        Initialize a base mnemonic.

        Args:
            name: Assembly instruction name.
            validator: Strategy for validating operands.
            comment_generator: Strategy for generating comments.
            *operands: Variable number of instruction operands.
            enable_comment: Whether to generate comments in output.

        Raises:
            TypeError: If any operand has invalid type.
            ValueError: If operands fail validation.

        """
        self.name = name
        self.operands = [Operand(op) for op in operands]
        self.validator = validator
        self.comment_generator = comment_generator or DefaultCommentGenerator()
        self.enable_comment = enable_comment
        self.custom_comment: str | None = None

        self._validate_operand_types()
        self.validator.validate(self.operands)

    def _validate_operand_types(self) -> None:
        """
        Validate operand types against allowed types.

        Allowed types are Register, str, and int.

        Raises:
            TypeError: If any operand has invalid type.

        """
        allowed_types: tuple[type[Register], type[str], type[int]] = (
            Register,
            str,
            int,
        )
        for i, operand in enumerate(self.operands, 1):
            if not isinstance(operand.value, allowed_types):
                raise TypeError(
                    f"Operand {i} has invalid type {type(operand.value).__name__}. "
                    f"Allowed types: Register, str, int."
                )

    @property
    def comment(self) -> str | None:
        """
        Get the current comment for the instruction.

        Returns:
            Current comment string or None if no custom comment is set.

        """
        return self.custom_comment

    @comment.setter
    def comment(self, value: str | None) -> None:
        """
        Set a custom comment or reset to default.

        Args:
            value: Custom comment string or None to use generated comment.

        """
        self.custom_comment = value

    def _format_operands(self) -> str:
        """
        Format operands for instruction assembly.

        Returns:
            Comma-separated string of operands.

        """
        return ", ".join(str(op) for op in self.operands)

    def construct(self, indent: str = "") -> str:
        """
        Construct complete assembly instruction string.

        This method generates the final assembly instruction with proper formatting,
        including indentation and optional comments.

        Args:
            indent: Leading indentation for the instruction.

        Returns:
            Formatted assembly instruction with optional comment.

        """
        instruction: str = self.name
        if self.operands:
            instruction += " " + self._format_operands()

        if self.enable_comment:
            comment: str = self.custom_comment or self.comment_generator.generate(
                self.name, self.operands
            )
            return f"{indent}{instruction}    ; {comment}"

        return f"{indent}{instruction}"


class TwoOperandValidator(OperandValidator):
    """
    Validator for instructions requiring exactly 2 operands.

    This validator ensures that instructions like ADD, SUB, etc.
    receive the correct number of operands.

    Attributes:
        mnemonic_name: Name of the mnemonic being validated.

    """

    def __init__(self, mnemonic_name: str) -> None:
        """
        Initialize two-operand validator.

        Args:
            mnemonic_name: Name of the mnemonic for error messages.

        """
        self.mnemonic_name = mnemonic_name

    def validate(self, operands: list[Operand]) -> None:
        """
        Validate that exactly 2 operands are provided.

        Args:
            operands: List of operands to validate.

        Raises:
            ValueError: If number of operands is not exactly 2.

        """
        if len(operands) != 2:
            raise ValueError(
                f"Mnemonic {self.mnemonic_name.upper()} requires 2 operands; "
                f"got {len(operands)}"
            )


class OneOperandValidator(OperandValidator):
    """
    Validator for instructions requiring exactly 1 operand.

    This validator ensures that instructions like INC, DEC, etc.
    receive the correct number of operands.

    Attributes:
        mnemonic_name: Name of the mnemonic being validated.

    """

    def __init__(self, mnemonic_name: str) -> None:
        """
        Initialize one-operand validator.

        Args:
            mnemonic_name: Name of the mnemonic for error messages.

        """
        self.mnemonic_name = mnemonic_name

    def validate(self, operands: list[Operand]) -> None:
        """
        Validate that exactly 1 operand is provided.

        Args:
            operands: List of operands to validate.

        Raises:
            ValueError: If number of operands is not exactly 1.

        """
        if len(operands) != 1:
            raise ValueError(
                f"Mnemonic {self.mnemonic_name.upper()} requires 1 operand; "
                f"got {len(operands)}"
            )
