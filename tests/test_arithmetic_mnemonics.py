import pytest

from ngpasm.mnemonics.arithmetic import AddMnemonic
from ngpasm.registers import Register


class MockRegister(Register):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


@pytest.fixture
def add_mnemonic():
    return AddMnemonic("add", MockRegister("AX"), MockRegister("BX"))


def test_add_mnemonic_comment(add_mnemonic):
    assert add_mnemonic._generate_default_comment() == "Add from BX to AX"


@pytest.mark.parametrize(
    "operands",
    [
        [MockRegister("AX")],
    ],
)
def test_add_invalid_operands(operands):
    mnemonic = AddMnemonic("add", *operands)
    with pytest.raises(IndexError):
        mnemonic._generate_default_comment()
