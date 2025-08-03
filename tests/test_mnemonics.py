# test_mnemonics.py
import pytest

from ngpasm.mnemonics.base import _ABCBasicMnemonic, _BasicMnemonic
from ngpasm.registers import Register


class MockRegister(Register):
    def __init__(self, name, size=64):
        super().__init__(name, size)


class ConcreteMnemonic(_ABCBasicMnemonic):
    """Concrete implementation for testing base functionality"""

    def _validate(self):
        pass  # No validation for base tests


def test_abstract_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        _ABCBasicMnemonic("test")


def test_concrete_mnemonic_validation():
    # Should not raise with no validation
    ConcreteMnemonic("mov", "RAX", "RBX", "RCX")


def test_basic_mnemonic():
    mnemonic = _BasicMnemonic("nop")
    assert mnemonic.mnemonic_name == "nop"
    assert len(mnemonic.operands) == 0


def test_comment_property():
    mnemonic = ConcreteMnemonic("test")
    assert mnemonic.comment is None

    mnemonic.comment = "Custom comment"
    assert mnemonic.comment == "Custom comment"

    mnemonic.comment = None
    assert mnemonic.comment is None


def test_generate_default_comment():
    # No operands
    mnemonic = ConcreteMnemonic("ret")
    assert "RET operation." in mnemonic._generate_default_comment()

    # One operand
    mnemonic = ConcreteMnemonic("push", "RAX")
    assert "PUSH operand RAX." in mnemonic._generate_default_comment()

    # Two operands
    mnemonic = ConcreteMnemonic("mov", "RAX", "RBX")
    assert "MOV from RBX to RAX." in mnemonic._generate_default_comment()

    # Three operands
    mnemonic = ConcreteMnemonic("add", "RAX", "RBX", "RCX")
    assert "ADD with 3 operands." in mnemonic._generate_default_comment()


def test_format_operands():
    mnemonic = ConcreteMnemonic("mov", "RAX", 42, "[MEM]")
    assert mnemonic._format_operands() == "RAX, 42, [MEM]"


def test_construct_with_comment():
    mnemonic = ConcreteMnemonic("add", "RAX", "RBX", enable_comment=True)
    result = mnemonic.construct()
    assert result.startswith("add RAX, RBX")
    assert "; ADD from RBX to RAX." in result


def test_construct_with_custom_comment():
    mnemonic = ConcreteMnemonic("sub", "RCX", 10)
    mnemonic.comment = "Custom subtraction"
    result = mnemonic.construct()
    assert "; Custom subtraction" in result


def test_construct_without_comment():
    mnemonic = ConcreteMnemonic("inc", "counter", enable_comment=False)
    assert mnemonic.construct() == "inc counter"


def test_construct_with_indent():
    mnemonic = ConcreteMnemonic("dec", "index", enable_comment=False)
    result = mnemonic.construct("    ")
    assert result == "    dec index"
