import pytest

from ngpasm.registers import (
    BaseRegisterSet,
    Register,
    RegisterSet16,
    RegisterSet32,
    RegisterSet64,
    get_registers,
)


def test_register_creation() -> None:
    """Test Register dataclass creation and properties."""
    reg = Register("TEST", 64)
    assert reg.name == "TEST"  # noqa: S101
    assert reg.size == 64  # noqa: S101
    assert reg.aliases == frozenset()  # noqa: S101
    assert reg.parent is None  # noqa: S101


def test_register_validation() -> None:
    """Test Register size validation."""
    with pytest.raises(ValueError):  # noqa: PT011
        Register("INVALID", 128)


def test_register_hierarchy() -> None:
    """Test register parent-child relationships."""
    parent = Register("PARENT", 64)
    child = Register("CHILD", 32, parent=parent)

    assert child.parent == parent  # noqa: S101
    assert parent in child.get_full_hierarchy()  # noqa: S101


def test_base_register_set_abstract() -> None:
    """Test BaseRegisterSet is abstract."""
    with pytest.raises(NotImplementedError):  # noqa: PT012

        class TestSet(BaseRegisterSet):
            def _build_register_set(self) -> None:
                super()._build_register_set()

        TestSet(64)


def test_register_set16_creation() -> None:
    """Test 16-bit register set creation."""
    regs = RegisterSet16(16)
    assert isinstance(regs, BaseRegisterSet)  # noqa: S101
    assert regs.bitness == 16  # noqa: S101
    assert len(regs) == 21  # noqa: S101


def test_register_set32_creation() -> None:
    """Test 32-bit register set creation."""
    regs = RegisterSet32(32)
    assert isinstance(regs, BaseRegisterSet)  # noqa: S101
    assert regs.bitness == 32  # noqa: S101
    assert len(regs) == 35  # noqa: S101


def test_register_set64_creation() -> None:
    """Test 64-bit register set creation."""
    regs = RegisterSet64(64)
    assert isinstance(regs, BaseRegisterSet)  # noqa: S101
    assert regs.bitness == 64  # noqa: S101
    assert len(regs) == 76  # noqa: S101


def test_aliases_in_standard_sets() -> None:
    """Test aliases handling in standard register sets."""
    # Test 16-bit set
    regs16 = RegisterSet16(16)
    assert regs16["AX_ALIAS"].name == "AX"  # noqa: S101

    # Test 32-bit set
    regs32 = RegisterSet32(32)
    assert regs32["EAX_ALIAS"].name == "EAX"  # noqa: S101

    # Test 64-bit set
    regs64 = RegisterSet64(64)
    assert regs64["RAX_ALIAS"].name == "RAX"  # noqa: S101


def test_empty_aliases() -> None:
    """Test register with empty aliases set."""
    reg = Register("TEST", 64, aliases=frozenset())

    # Simulate adding to a register set
    class TestSet(BaseRegisterSet):
        def _build_register_set(self) -> None:
            self._registers = {"TEST": reg}

    regs = TestSet(64)
    assert "TEST" in regs  # noqa: S101
    assert regs.get("TEST") == reg  # noqa: S101
    assert regs.get("NON_EXISTENT") is None  # noqa: S101


@pytest.mark.parametrize(
    ("mode", "expected_type"),
    [
        ("16", RegisterSet16),
        ("32", RegisterSet32),
        ("64", RegisterSet64),
        ("", None),
        ("128", None),
        (16, None),
        (None, None),
    ],
)
def test_get_registers(mode: str, expected_type: type) -> None:
    """Test get_registers with valid and invalid modes."""
    result = get_registers(mode)
    if expected_type:
        assert isinstance(result, expected_type)  # noqa: S101
    else:
        assert result is None  # noqa: S101


def test_register_access() -> None:
    """Test register access methods."""
    regs = RegisterSet64(64)

    # Valid access
    assert regs["RAX"].name == "RAX"  # noqa: S101
    assert regs["EAX"].name == "EAX"  # noqa: S101
    assert regs["AX"].name == "AX"  # noqa: S101
    assert regs["AL"].name == "AL"  # noqa: S101

    # Case sensitivity
    with pytest.raises(KeyError):
        _ = regs["rax"]

    # get() method with default
    assert regs.get("rax") is not None  # noqa: S101
    assert regs.get("INVALID") is None  # noqa: S101
    assert regs.get("RAX").name == "RAX"  # noqa: S101


def test_register_hierarchy_in_set() -> None:
    """Test register hierarchy within a set."""
    regs = RegisterSet64(64)
    rax = regs["RAX"]
    al = regs["AL"]

    # Test hierarchy from bottom-up
    hierarchy = al.get_full_hierarchy()
    assert rax in hierarchy  # noqa: S101


@pytest.mark.parametrize(
    ("mode", "reg_name", "expected_size"),
    [
        ("16", "AX", 16),
        ("16", "AL", 8),
        ("32", "EAX", 32),
        ("32", "AX", 16),
        ("64", "RAX", 64),
        ("64", "EAX", 32),
        ("64", "R15B", 8),
    ],
)
def test_register_sizes(mode: str, reg_name: str, expected_size: int) -> None:
    """Test register sizes in different modes."""
    regs = get_registers(mode)
    assert regs is not None  # noqa: S101
    assert regs[reg_name].size == expected_size  # noqa: S101


@pytest.mark.parametrize(
    ("mode", "invalid_reg"),
    [("16", "EAX"), ("16", "R8"), ("32", "RAX"), ("32", "R8D"), ("64", "INVALID")],
)
def test_invalid_registers(mode: str, invalid_reg: str) -> None:
    """Test that invalid registers are not present."""
    regs = get_registers(mode)
    assert regs is not None  # noqa: S101
    assert regs.get(invalid_reg) is None  # noqa: S101


def test_register_aliases() -> None:
    """Test register alias support."""
    # Create register with alias
    reg = Register("TEST", 64, aliases=frozenset(["ALT1", "ALT2"]))

    # Simulate adding to a register set
    class TestSet(BaseRegisterSet):
        def _build_register_set(self) -> None:
            self._registers = {"TEST": reg, "ALT1": reg, "ALT2": reg}

    regs = TestSet(64)
    assert regs["TEST"] == reg  # noqa: S101
    assert regs["ALT1"] == reg  # noqa: S101
    assert regs["ALT2"] == reg  # noqa: S101
    assert reg == regs.ALT2  # noqa: S101
    assert reg == regs.TEST  # noqa: S101
    assert reg == regs.ALT1  # noqa: S101


def test_register_set_iteration() -> None:
    """Test iteration over register set."""
    regs = RegisterSet16(16)
    names = list(regs)
    assert "AX" in names  # noqa: S101
    assert "AL" in names  # noqa: S101
    assert "CS" in names  # noqa: S101
    assert len(names) == len(regs)  # noqa: S101


def test_register_set_contains() -> None:
    """Test contains method."""
    regs = RegisterSet32(32)
    assert regs.contains("EAX")  # noqa: S101
    assert regs.contains("eax")  # noqa: S101
    assert not regs.contains("INVALID")  # noqa: S101
