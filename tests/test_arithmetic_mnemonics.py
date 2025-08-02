# [file name]: tests/test_arithmetic_mnemonics.py
import pytest

from ngpasm.mnemonics.arithmetic import (
    AddMnemonic,
    DecMnemonic,
    DivMnemonic,
    IncMnemonic,
    MulMnemonic,
    SubMnemonic,
)
from ngpasm.registers import Register


class MockRegister(Register):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


AX = MockRegister("AX")
BX = MockRegister("BX")
CX = MockRegister("CX")
DX = MockRegister("DX")


@pytest.fixture
def add_mnemonic():
    return AddMnemonic("add", AX, BX)


@pytest.fixture
def sub_mnemonic():
    return SubMnemonic("sub", AX, BX)


@pytest.fixture
def div_mnemonic():
    return DivMnemonic("div", AX, BX)


@pytest.fixture
def mul_mnemonic():
    return MulMnemonic("mul", AX, BX)


@pytest.fixture
def inc_mnemonic():
    return IncMnemonic("inc", AX)


@pytest.fixture
def dec_mnemonic():
    return DecMnemonic("dec", AX)


def test_add_mnemonic_comment(add_mnemonic):
    assert add_mnemonic._generate_default_comment() == "Adding the BX value to the AX"


@pytest.mark.parametrize("operands", [[AX], [AX, BX, CX], [], [10]])
def test_add_invalid_operands(operands):
    with pytest.raises(ValueError) as excinfo:
        AddMnemonic("add", *operands)
    assert "operands" in str(excinfo.value)


def test_sub_mnemonic_comment(sub_mnemonic):
    assert (
        sub_mnemonic._generate_default_comment() == "Substract the BX value to the AX"
    )


@pytest.mark.parametrize("operands", [[AX], [AX, BX, CX], []])
def test_sub_invalid_operands(operands):
    with pytest.raises(ValueError) as excinfo:
        SubMnemonic("sub", *operands)
    assert "operands" in str(excinfo.value)


def test_div_mnemonic_comment(div_mnemonic):
    assert div_mnemonic._generate_default_comment() == "Divising the BX value to the AX"


@pytest.mark.parametrize("operands", [[AX], [AX, BX, CX], []])
def test_div_invalid_operands(operands):
    with pytest.raises(ValueError) as excinfo:
        DivMnemonic("div", *operands)
    assert "operands" in str(excinfo.value)


def test_mul_mnemonic_comment(mul_mnemonic):
    assert (
        mul_mnemonic._generate_default_comment()
        == "Multiplicating the BX value to the AX"
    )


@pytest.mark.parametrize("operands", [[AX], [AX, BX, CX], []])
def test_mul_invalid_operands(operands):
    with pytest.raises(ValueError) as excinfo:
        MulMnemonic("mul", *operands)
    assert "operands" in str(excinfo.value)


def test_inc_mnemonic_comment(inc_mnemonic):
    assert inc_mnemonic._generate_default_comment() == "Increment AX"


@pytest.mark.parametrize("operands", [[], [AX, BX], [AX, BX, CX]])
def test_inc_invalid_operands(operands):
    with pytest.raises(ValueError) as excinfo:
        IncMnemonic("inc", *operands)
    assert "operands" in str(excinfo.value)


def test_dec_mnemonic_comment(dec_mnemonic):
    assert dec_mnemonic._generate_default_comment() == "Decrement AX"


@pytest.mark.parametrize("operands", [[], [AX, BX], [AX, BX, CX]])
def test_dec_invalid_operands(operands):
    with pytest.raises(ValueError) as excinfo:
        DecMnemonic("dec", *operands)
    assert "operands" in str(excinfo.value)


@pytest.mark.parametrize(
    ("mnemonic_class", "operands"),
    [
        (AddMnemonic, [AX, BX]),
        (SubMnemonic, [AX, CX]),
        (DivMnemonic, [DX, AX]),
        (MulMnemonic, [BX, CX]),
        (IncMnemonic, [AX]),
        (DecMnemonic, [BX]),
    ],
)
def test_valid_operands(mnemonic_class, operands):
    instance = mnemonic_class("test", *operands)
    assert len(instance.operands) == len(operands)


@pytest.mark.parametrize(
    ("mnemonic_class", "invalid_operands"),
    [
        (AddMnemonic, [None, BX]),
        (SubMnemonic, [AX, 3.14]),
        (DivMnemonic, [object(), BX]),
        (MulMnemonic, [AX, [1, 2]]),
        (IncMnemonic, [set()]),
        (DecMnemonic, [3.14]),
    ],
)
def test_invalid_operand_types(mnemonic_class, invalid_operands):
    with pytest.raises(TypeError):
        mnemonic = mnemonic_class("test", *invalid_operands)
        mnemonic._validate_operand_types()


def test_add_construction(add_mnemonic):
    add_mnemonic.comment = "Custom addition"
    result = add_mnemonic.construct()
    assert result == "    add AX, BX  ; Custom addition"


def test_inc_construction(inc_mnemonic):
    inc_mnemonic._enable_comment = False
    assert inc_mnemonic.construct() == "    inc AX"


def test_mul_construction(mul_mnemonic):
    assert mul_mnemonic.construct().startswith("    mul AX, BX")


def test_construct_with_default_comment(inc_mnemonic):
    result = inc_mnemonic.construct()
    assert "Increment AX" in result


def test_construct_with_disabled_comment(inc_mnemonic):
    inc_mnemonic._enable_comment = False
    assert ";" not in inc_mnemonic.construct()


def test_construct_with_custom_indent(inc_mnemonic):
    result = inc_mnemonic.construct(indent="  ")
    assert result.startswith("  inc AX")
