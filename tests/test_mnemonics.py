import pytest

from ngpasm.mnemonics.base import _ABCBasicMnemonic, _BasicMnemonic
from ngpasm.registers import Register


class MockRegister(Register):  # noqa: D101
    def __init__(self, name):  # noqa: D107
        self.name = name

    def __str__(self):  # noqa: D105
        return self.name


class _TestBasicMnemonic(_ABCBasicMnemonic):
    def _validate(self):
        raise NotImplementedError


def test_validate_not_implemented():
    """Test that abstract class requires _validate implementation."""
    with pytest.raises(NotImplementedError):
        _TestBasicMnemonic("mov", "eax", "ebx", enable_comment=True)


@pytest.fixture
def basic_mnemonic():  # noqa: D103
    return _BasicMnemonic(
        "test", MockRegister("AX"), MockRegister("BX"), enable_comment=True
    )


@pytest.mark.parametrize(
    ("operands", "expected"),
    [
        ([], "TEST operation."),
        (["AX"], "TEST operand AX."),
        (["AX", "BX"], "TEST from BX to AX."),
        (["AX", "BX", 10], "TEST with 3 operands."),
    ],
)
def test_generate_default_comment(operands, expected):  # noqa: D103
    mnemonic = _BasicMnemonic("test", *operands)
    assert mnemonic._generate_default_comment() == expected  # noqa: S101, SLF001


def test_comment_property(basic_mnemonic):  # noqa: D103
    basic_mnemonic.comment = "Custom comment"
    assert basic_mnemonic.comment == "Custom comment"  # noqa: S101

    basic_mnemonic.comment = None
    assert basic_mnemonic.comment is None  # noqa: S101


@pytest.mark.parametrize(
    "operands",
    [
        [MockRegister("AX"), "BX"],
        ["AX", 10],
        [10, MockRegister("BX")],
    ],
)
def test_valid_operand_types(operands):  # noqa: D103
    mnemonic = _BasicMnemonic("test", *operands)
    mnemonic._validate_operand_types()  # noqa: SLF001


@pytest.mark.parametrize(
    "operands",
    [
        [None],
        [3.14],
        [object()],
    ],
)
def test_invalid_operand_types(operands):  # noqa: D103
    with pytest.raises(TypeError):  # noqa: PT012
        mnemonic = _BasicMnemonic("test", *operands)
        mnemonic._validate_operand_types()  # noqa: SLF001


@pytest.mark.parametrize(
    ("operands", "expected"),
    [
        ([], ""),
        (["AX"], "AX"),
        (["AX", 10], "AX, 10"),
        (["AX", "BX", 10], "AX, BX, 10"),
    ],
)
def test_format_operands(operands, expected):  # noqa: D103
    mnemonic = _BasicMnemonic("test", *operands)
    assert mnemonic._format_operands() == expected  # noqa: S101, SLF001


@pytest.mark.parametrize(
    ("enable_comment", "comment", "expected"),
    [
        (True, None, "    test AX, BX  ; TEST from BX to AX."),
        (True, "Custom", "    test AX, BX  ; Custom"),
        (False, None, "    test AX, BX"),
    ],
)
def test_construct(basic_mnemonic, enable_comment, comment, expected):  # noqa: D103
    basic_mnemonic._enable_comment = enable_comment  # noqa: SLF001
    basic_mnemonic.comment = comment
    assert basic_mnemonic.construct() == expected  # noqa: S101


def test_construct_indent(basic_mnemonic):  # noqa: D103
    assert (  # noqa: S101
        basic_mnemonic.construct(indent="  ") == "  test AX, BX  ; TEST from BX to AX."
    )


def test_construct_no_operands():  # noqa: D103
    mnemonic = _BasicMnemonic("nop")
    assert mnemonic.construct() == "    nop  ; NOP operation."  # noqa: S101
