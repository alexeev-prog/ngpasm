import pytest

from ngpasm.mnemonics.base import _BasicMnemonic
from ngpasm.registers import Register


class MockRegister(Register):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


@pytest.fixture
def basic_mnemonic():
    return _BasicMnemonic(
        "test", MockRegister("AX"), MockRegister("BX"), enable_comment=True
    )


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([], "TEST operation."),
        (["AX"], "TEST operand AX."),
        (["AX", "BX"], "TEST from BX to AX."),
        (["AX", "BX", 10], "TEST with 3 operands."),
    ],
)
def test_generate_default_comment(operands, expected):
    mnemonic = _BasicMnemonic("test", *operands)
    assert mnemonic._generate_default_comment() == expected


def test_comment_property(basic_mnemonic):
    basic_mnemonic.comment = "Custom comment"
    assert basic_mnemonic.comment == "Custom comment"

    basic_mnemonic.comment = None
    assert basic_mnemonic.comment is None


@pytest.mark.parametrize(
    "operands",
    [
        [MockRegister("AX"), "BX"],
        ["AX", 10],
        [10, MockRegister("BX")],
    ],
)
def test_valid_operand_types(operands):
    mnemonic = _BasicMnemonic("test", *operands)
    mnemonic._validate_operand_types()


@pytest.mark.parametrize(
    "operands",
    [
        [None],
        [3.14],
        [object()],
    ],
)
def test_invalid_operand_types(operands):
    with pytest.raises(TypeError):
        mnemonic = _BasicMnemonic("test", *operands)
        mnemonic._validate_operand_types()


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([], ""),
        (["AX"], "AX"),
        (["AX", 10], "AX, 10"),
        (["AX", "BX", 10], "AX, BX, 10"),
    ],
)
def test_format_operands(operands, expected):
    mnemonic = _BasicMnemonic("test", *operands)
    assert mnemonic._format_operands() == expected


@pytest.mark.parametrize(
    "enable_comment, comment, expected",
    [
        (True, None, "    test AX, BX  ; TEST from BX to AX."),
        (True, "Custom", "    test AX, BX  ; Custom"),
        (False, None, "    test AX, BX"),
    ],
)
def test_construct(basic_mnemonic, enable_comment, comment, expected):
    basic_mnemonic._enable_comment = enable_comment
    basic_mnemonic.comment = comment
    assert basic_mnemonic.construct() == expected


def test_construct_indent(basic_mnemonic):
    assert (
        basic_mnemonic.construct(indent="  ") == "  test AX, BX  ; TEST from BX to AX."
    )


def test_construct_no_operands():
    mnemonic = _BasicMnemonic("nop")
    assert mnemonic.construct() == "    nop  ; NOP operation."
