import pytest

from ngpasm.mnemonics.arithmetic import AddMnemonic
from ngpasm.registers import Register


class MockRegister(Register):  # noqa: D101
    def __init__(self, name):  # noqa: D107
        self.name = name

    def __str__(self):  # noqa: D105
        return self.name


@pytest.fixture
def add_mnemonic():  # noqa: D103
    return AddMnemonic("add", MockRegister("AX"), MockRegister("BX"))


def test_add_mnemonic_comment(add_mnemonic):  # noqa: D103
    assert add_mnemonic._generate_default_comment() == "Adding the BX value to the AX"  # noqa: S101, SLF001


@pytest.mark.parametrize(
    "operands",
    [
        [MockRegister("AX")],
    ],
)
def test_add_invalid_operands(operands):  # noqa: D103
    with pytest.raises(IndexError):
        mnemonic = AddMnemonic("add", *operands)  # noqa: F841
