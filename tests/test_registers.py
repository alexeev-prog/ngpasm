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
    assert reg.name == "TEST"
    assert reg.size == 64
    assert reg.aliases == frozenset()
    assert reg.parent is None


def test_register_validation() -> None:
    """Test Register size validation."""
    with pytest.raises(ValueError):
        Register("INVALID", 128)


def test_register_hierarchy() -> None:
    """Test register parent-child relationships."""
    parent = Register("PARENT", 64)
    child = Register("CHILD", 32, parent=parent)

    assert child.parent == parent
    assert parent in child.get_full_hierarchy()


def test_base_register_set_abstract() -> None:
    """Test BaseRegisterSet is abstract."""
    with pytest.raises(NotImplementedError):

        class TestSet(BaseRegisterSet):
            def _build_register_set(self) -> None:
                super()._build_register_set()

        TestSet(64)


def test_register_set16_creation() -> None:
    """Test 16-bit register set creation."""
    regs = RegisterSet16(16)
    assert isinstance(regs, BaseRegisterSet)
    assert regs.bitness == 16
    assert len(regs) == 21


def test_register_set32_creation() -> None:
    """Test 32-bit register set creation."""
    regs = RegisterSet32(32)
    assert isinstance(regs, BaseRegisterSet)
    assert regs.bitness == 32
    assert len(regs) == 35  # Updated count (added EAX_ALIAS)


def test_register_set64_creation() -> None:
    """Test 64-bit register set creation."""
    regs = RegisterSet64(64)
    assert isinstance(regs, BaseRegisterSet)
    assert regs.bitness == 64
    assert len(regs) == 76  # Updated count (added RAX_ALIAS)


def test_aliases_in_standard_sets() -> None:
    """Test aliases handling in standard register sets."""
    # Test 16-bit set
    regs16 = RegisterSet16(16)
    assert regs16["AX_ALIAS"].name == "AX"

    # Test 32-bit set
    regs32 = RegisterSet32(32)
    assert regs32["EAX_ALIAS"].name == "EAX"

    # Test 64-bit set
    regs64 = RegisterSet64(64)
    assert regs64["RAX_ALIAS"].name == "RAX"


def test_empty_aliases() -> None:
    """Test register with empty aliases set."""
    reg = Register("TEST", 64, aliases=frozenset())

    # Simulate adding to a register set
    class TestSet(BaseRegisterSet):
        def _build_register_set(self) -> None:
            self._registers = {"TEST": reg}

    regs = TestSet(64)
    assert "TEST" in regs
    assert regs.get("TEST") == reg
    assert regs.get("NON_EXISTENT") is None


@pytest.mark.parametrize(
    "mode, expected_type",
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
        assert isinstance(result, expected_type)
    else:
        assert result is None


def test_register_access() -> None:
    """Test register access methods."""
    regs = RegisterSet64(64)

    # Valid access
    assert regs["RAX"].name == "RAX"
    assert regs["EAX"].name == "EAX"
    assert regs["AX"].name == "AX"
    assert regs["AL"].name == "AL"

    # Case sensitivity
    with pytest.raises(KeyError):
        _ = regs["rax"]

    # get() method with default
    assert regs.get("rax") is not None  # Updated expectation
    assert regs.get("INVALID") is None
    assert regs.get("RAX").name == "RAX"  # type: ignore


def test_register_hierarchy_in_set() -> None:
    """Test register hierarchy within a set."""
    regs = RegisterSet64(64)
    rax = regs["RAX"]
    al = regs["AL"]

    # Test hierarchy from bottom-up
    hierarchy = al.get_full_hierarchy()
    assert rax in hierarchy


@pytest.mark.parametrize(
    "mode, reg_name, expected_size",
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
    assert regs is not None
    assert regs[reg_name].size == expected_size


@pytest.mark.parametrize(
    "mode, invalid_reg",
    [("16", "EAX"), ("16", "R8"), ("32", "RAX"), ("32", "R8D"), ("64", "INVALID")],
)
def test_invalid_registers(mode: str, invalid_reg: str) -> None:
    """Test that invalid registers are not present."""
    regs = get_registers(mode)
    assert regs is not None
    assert regs.get(invalid_reg) is None


def test_register_aliases() -> None:
    """Test register alias support."""
    # Create register with alias
    reg = Register("TEST", 64, aliases=frozenset(["ALT1", "ALT2"]))

    # Simulate adding to a register set
    class TestSet(BaseRegisterSet):
        def _build_register_set(self) -> None:
            self._registers = {"TEST": reg, "ALT1": reg, "ALT2": reg}

    regs = TestSet(64)
    assert regs["TEST"] == reg
    assert regs["ALT1"] == reg
    assert regs["ALT2"] == reg
    assert reg == regs.ALT2
    assert reg == regs.TEST
    assert reg == regs.ALT1


def test_register_set_iteration() -> None:
    """Test iteration over register set."""
    regs = RegisterSet16(16)
    names = list(regs)
    assert "AX" in names
    assert "AL" in names
    assert "CS" in names
    assert len(names) == len(regs)


def test_register_set_contains() -> None:
    """Test contains method."""
    regs = RegisterSet32(32)
    assert regs.contains("EAX")
    assert regs.contains("eax")  # Updated expectation
    assert not regs.contains("INVALID")
