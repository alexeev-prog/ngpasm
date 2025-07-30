from ngpasm.mnemonics.base import _BasicMnemonic


class AddMnemonic(_BasicMnemonic):
    """Add arithmetic mnemonic."""

    def _generate_default_comment(self) -> str:
        return f"Add from {self.operands[1]!s} to {self.operands[0]!s}"
