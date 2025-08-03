# test_arithmetic_mnemonics.py
import pytest

from ngpasm.mnemonics.arithmetic import (
    AddMnemonic,
    SubMnemonic,
    DivMnemonic,
    MulMnemonic,
    IncMnemonic,
    DecMnemonic,
)
from ngpasm.registers import Register


class MockRegister(Register):
    def __init__(self, name, size=64):
        super().__init__(name, size)


@pytest.fixture
def mock_registers():
    return [
        MockRegister("RAX"),
        MockRegister("RBX"),
        MockRegister("RCX"),
        MockRegister("AL"),
    ]


def test_add_mnemonic_validation(mock_registers):
    # Valid
    AddMnemonic(mock_registers[0], mock_registers[1])

    # Invalid operand count
    with pytest.raises(ValueError):
        AddMnemonic(mock_registers[0])
    with pytest.raises(ValueError):
        AddMnemonic(mock_registers[0], mock_registers[1], mock_registers[2])


def test_add_mnemonic_comment(mock_registers):
    mnemonic = AddMnemonic(mock_registers[0], mock_registers[1])
    assert "Adding the RBX value to the RAX" in mnemonic._generate_default_comment()


def test_sub_mnemonic_validation(mock_registers):
    # Valid
    SubMnemonic(mock_registers[0], mock_registers[1])

    # Invalid operand count
    with pytest.raises(ValueError):
        SubMnemonic(mock_registers[0])
    with pytest.raises(ValueError):
        SubMnemonic(mock_registers[0], mock_registers[1], mock_registers[2])


def test_sub_mnemonic_comment(mock_registers):
    mnemonic = SubMnemonic(mock_registers[0], mock_registers[1])
    assert "Subtract the RBX value from the RAX" in mnemonic._generate_default_comment()


def test_div_mnemonic_validation(mock_registers):
    # Valid
    DivMnemonic(mock_registers[0], mock_registers[1])

    # Invalid operand count
    with pytest.raises(ValueError):
        DivMnemonic(mock_registers[0])
    with pytest.raises(ValueError):
        DivMnemonic(mock_registers[0], mock_registers[1], mock_registers[2])


def test_div_mnemonic_comment(mock_registers):
    mnemonic = DivMnemonic(mock_registers[0], mock_registers[1])
    assert "Dividing the RBX value to the RAX" in mnemonic._generate_default_comment()


def test_mul_mnemonic_validation(mock_registers):
    # Valid
    MulMnemonic(mock_registers[0], mock_registers[1])

    # Invalid operand count
    with pytest.raises(ValueError):
        MulMnemonic(mock_registers[0])
    with pytest.raises(ValueError):
        MulMnemonic(mock_registers[0], mock_registers[1], mock_registers[2])


def test_mul_mnemonic_comment(mock_registers):
    mnemonic = MulMnemonic(mock_registers[0], mock_registers[1])
    assert "Multiplicating the RBX value to the RAX" in mnemonic._generate_default_comment()


def test_inc_mnemonic_validation(mock_registers):
    # Valid
    IncMnemonic(mock_registers[0])

    # Invalid operand count
    with pytest.raises(ValueError):
        IncMnemonic()
    with pytest.raises(ValueError):
        IncMnemonic(mock_registers[0], mock_registers[1])


def test_inc_mnemonic_comment(mock_registers):
    mnemonic = IncMnemonic(mock_registers[0])
    assert "Increment RAX" in mnemonic._generate_default_comment()


def test_dec_mnemonic_validation(mock_registers):
    # Valid
    DecMnemonic(mock_registers[0])

    # Invalid operand count
    with pytest.raises(ValueError):
        DecMnemonic()
    with pytest.raises(ValueError):
        DecMnemonic(mock_registers[0], mock_registers[1])


def test_dec_mnemonic_comment(mock_registers):
    mnemonic = DecMnemonic(mock_registers[0])
    assert "Decrement RAX" in mnemonic._generate_default_comment()


def test_arithmetic_mnemonics_with_non_register_operands():
    # Test with mixed operand types
    AddMnemonic("RAX", 42)
    SubMnemonic(Register("RBX", 64), "value")
    MulMnemonic(100, Register("RCX", 64))
    DivMnemonic("[MEM]", Register("RDX", 64))
    IncMnemonic("counter")
    DecMnemonic(42)


def test_arithmetic_mnemonics_invalid_operand_types():
    # Must call construct() to trigger type validation
    with pytest.raises(TypeError):
        AddMnemonic(3.14, Register("RAX", 64)).construct()

    with pytest.raises(TypeError):
        SubMnemonic(Register("RAX", 64), [1, 2, 3]).construct()
