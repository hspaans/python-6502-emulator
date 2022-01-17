"""Verifies that the memory class works as expected."""
import pytest
import m6502


@pytest.mark.parametrize("i", range(0x0000, 0x0100))
def test_write_zero_page(i: int) -> None:
    """
    Verify that the Zero Page memory can be written to and read from.

    :param i: The address to write to
    :return: None
    """
    memory = m6502.Memory()
    memory[i] = 0xA5
    assert memory[i] == 0xA5


@pytest.mark.parametrize("i", range(0x0100, 0x0200))
def test_write_stack(i: int) -> None:
    """
    Verify that the Stack memory can be written to and read from.

    :param i: The address to write to
    :return: None
    """
    memory = m6502.Memory()
    memory[i] = 0xA5
    assert memory[i] == 0xA5


@pytest.mark.parametrize("i", [0xFFFC, 0xFFFD])
def test_write_vector(i: int) -> None:
    """
    Verify that the C64 vector memory can be written to and read from.

    :param i: The address to write to
    :return: None
    """
    memory = m6502.Memory()
    memory[i] = 0xA5
    assert memory[i] == 0xA5
