from abc import ABC, abstractmethod
from typing import Union

from ngpasm.registers import Register


class _ABCBasicMnemonic(ABC):
    """
    Base class for assembly mnemonics with flexible operand handling.

    This class provides core functionality for constructing assembly instructions
    with variable number of operands and automatic comment generation.

    Attributes:
        mnemonic_name: Assembly instruction name (e.g., 'mov', 'add').
        operands: Sequence of instruction operands.
        enable_comment: Flag to control comment generation.
        comment: Custom comment for the instruction.

    """

    def __init__(
        self,
        mnemonic_name: str,
        *operands: Union["Register", str, int],
        enable_comment: bool = True,
    ) -> None:
        """
        Initializes mnemonic with operands and comment settings.

        Args:
            mnemonic_name: Name of the assembly instruction.
            *operands: Variable-length sequence of instruction operands.
            enable_comment: Whether to generate comments in output.

        """
        self.mnemonic_name = mnemonic_name
        self.operands = operands
        self._enable_comment = enable_comment
        self._comment: str | None = None

        self._validate()

    @abstractmethod
    def _validate(self):
        """Validate mnemonics operands and other fields."""

    @property
    def comment(self) -> str | None:
        """Gets the current comment for the instruction."""
        return self._comment

    @comment.setter
    def comment(self, value: str | None) -> None:
        """
        Sets a custom comment or resets to default.

        Args:
            value: Custom comment string or None to use default.

        """
        self._comment = value

    def _generate_default_comment(self) -> str:
        """
        Generates context-sensitive default comment based on operands.

        Returns:
            Appropriately formatted comment string.

        """
        operand_count = len(self.operands)
        instruction = self.mnemonic_name.upper()

        if operand_count == 0:
            return f"{instruction} operation."
        if operand_count == 1:
            return f"{instruction} operand {self.operands[0]!s}."
        if operand_count == 2:
            return f"{instruction} from {self.operands[1]!s} to {self.operands[0]!s}."
        return f"{instruction} with {operand_count} operands."

    def _validate_operand_types(self) -> None:
        """
        Validates operand types against allowed types.

        Raises:
            TypeError: If any operand has invalid type.

        """
        allowed_types = (Register, str, int)
        for i, operand in enumerate(self.operands, 1):
            if not isinstance(operand, allowed_types):
                raise TypeError(
                    f"Operand {i} has invalid type {type(operand).__name__}. "
                    f"Allowed types: Register, str, int."
                )

    def _format_operands(self) -> str:
        """
        Formats operands for instruction assembly.

        Returns:
            Comma-separated operand string.

        """
        return ", ".join(str(op) for op in self.operands)

    def construct(self, indent: str = "") -> str:
        """
        Constructs complete assembly instruction string.

        Args:
            indent: Leading indentation for the instruction.

        Returns:
            Formatted assembly instruction with optional comment.

        """
        self._validate_operand_types()

        # Build instruction core
        instruction = self.mnemonic_name
        if self.operands:
            instruction += " " + self._format_operands()

        # Add comment if enabled
        if self._enable_comment:
            comment = self._comment or self._generate_default_comment()
            return f"{indent}{instruction}  ; {comment}"

        return f"{indent}{instruction}"


class _BasicMnemonic(_ABCBasicMnemonic):
    def _validate(self):
        pass
