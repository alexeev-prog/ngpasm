# test_program.py
import pytest

from ngpasm.mnemonics.base import _BasicMnemonic
from ngpasm.program import ASMProgram, ProgramMode


class MockMnemonic(_BasicMnemonic):
    """Mock mnemonic with comment disabled by default."""

    def __init__(self, mnemonic_name, *operands, enable_comment=False):
        super().__init__(mnemonic_name, *operands, enable_comment=enable_comment)


@pytest.fixture
def sample_program():
    return ASMProgram("test.asm", ProgramMode.x64bit)


def test_program_init(sample_program):
    assert sample_program.filename == "test.asm"
    assert sample_program.mode == ProgramMode.x64bit
    assert len(sample_program._mnemonics) == 0
    assert sample_program._current_indent_level == 0
    assert sample_program._indent == ""


def test_registers_property(sample_program):
    registers = sample_program.regs
    assert registers is not None
    assert registers["RAX"].name == "RAX"
    assert registers["EAX"].name == "EAX"
    assert registers["AL"].name == "AL"


def test_insert_mnemonic(sample_program):
    mnemonic = MockMnemonic("nop")
    sample_program.insert_mnemonic(mnemonic)
    assert len(sample_program._mnemonics) == 1
    assert sample_program._mnemonics[0] == mnemonic


def test_generate_empty_program(sample_program):
    assert sample_program.generate() == ""


def test_generate_single_mnemonic(sample_program):
    mnemonic = MockMnemonic("ret")
    sample_program.insert_mnemonic(mnemonic)
    assert sample_program.generate() == "ret"


def test_generate_multiple_mnemonics(sample_program):
    sample_program.insert_mnemonic(MockMnemonic("push", "RAX"))
    sample_program.insert_mnemonic(MockMnemonic("pop", "RBX"))

    result = sample_program.generate()
    assert "push RAX" in result
    assert "pop RBX" in result
    assert result.count("\n") == 1


def test_generate_with_indentation(sample_program):
    sample_program._indent = "    "
    sample_program.insert_mnemonic(MockMnemonic("mov", "RAX", "RBX"))
    assert sample_program.generate() == "    mov RAX, RBX"


def test_program_modes():
    program_16 = ASMProgram("test16.asm", ProgramMode.x16bit)
    assert program_16.regs["AX"].name == "AX"

    program_32 = ASMProgram("test32.asm", ProgramMode.x32bit)
    assert program_32.regs["EAX"].name == "EAX"

    program_64 = ASMProgram("test64.asm", ProgramMode.x64bit)
    assert program_64.regs["RAX"].name == "RAX"


def test_program_with_comments():
    program = ASMProgram("test.asm", ProgramMode.x64bit)
    mnemonic = MockMnemonic("add", "RAX", 10, enable_comment=True)
    program.insert_mnemonic(mnemonic)

    result = program.generate()
    assert "add RAX, 10" in result
    assert "; ADD from 10 to RAX." in result
