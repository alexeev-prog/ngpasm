from ngpasm.registers import Register


class _BasicMnemonic:
    def __init__(
        self,
        mnemonic_name: str,
        dest: Register | str | int | None = None,
        source: Register | str | int | None = None,
        *,
        enable_comment: bool = True,
    ):
        self.mnemonic_name = mnemonic_name
        self.dest = dest
        self.source = source
        self._enable_comment = enable_comment
        self.comment: str | None = self._generate_default_comment()

    def _generate_default_comment(self) -> str:
        return f"{self.mnemonic_name.upper()} from {self.source!s} into {self.dest!s}."

    def construct(self, indent: str) -> str:
        instruction = f"{indent}{self.mnemonic_name} {self.dest}, {self.source}"

        if self._enable_comment:
            instruction += f"  ; {self.comment}"

        return instruction

    def set_comment(self, comment: str | None) -> None:
        if comment is None:
            self.comment = self._generate_default_comment()
        else:
            self.comment = comment

