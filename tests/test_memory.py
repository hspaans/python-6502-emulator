import pytest
import m6502


@pytest.mark.parametrize("i", range(10))
def test_read_memory(i):
    """Verify read memory"""
    memory = m6502.Memory()
    assert memory[i] == 0x00


@pytest.mark.parametrize("i", range(10))
def test_write_memory(i):
    """Verify write memory"""
    memory = m6502.Memory()
    memory[i] = 0xF0
    assert memory[i] == 0xF0
