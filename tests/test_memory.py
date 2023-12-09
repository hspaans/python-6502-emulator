"""Verifies that the memory class works as expected."""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    "size", [
        0x0200,
        0xFFFF
    ])
def test_init_memory_size(size: int) -> None:
    """
    Verify with invalid memory sizes.

    TODO: Verify correct memory sizes

    :param size: The size of the memory
    :return: None
    """
    memory = Memory(size)  # noqa: E302 F841 PLW0612
    assert len(memory.memory) == size


@pytest.mark.parametrize(
    "size", [
        0x01FF,
        0x010000
    ])
def test_init_memory_valueerror(size: int) -> None:
    """
    Verify with invalid memory sizes.

    TODO: Verify correct memory sizes

    :param size: The size of the memory
    :return: None
    """
    with pytest.raises(ValueError, match="Memory size is not valid"):
        memory = Memory(size)  # noqa: E302 F841 PLW0612


@pytest.mark.parametrize(
    "i",
    range(0x0000, 0x0100)
)
def test_write_zero_page(i: int) -> None:
    """
    Verify that the Zero Page memory can be written to and read from.

    :param i: The address to write to
    :return: None
    """
    memory = Memory()
    memory[i] = 0xA5
    assert memory[i] == 0xA5


@pytest.mark.parametrize(
    "i",
    range(0x0100, 0x0200)
)
def test_write_stack(i: int) -> None:
    """
    Verify that the Stack memory can be written to and read from.

    :param i: The address to write to
    :return: None
    """
    memory = Memory()
    memory[i] = 0xA5
    assert memory[i] == 0xA5


@pytest.mark.parametrize(
    "i", [
        0xFFFC,
        0xFFFD
    ])
def test_write_vector(i: int) -> None:
    """
    Verify that the C64 vector memory can be written to and read from.

    :param i: The address to write to
    :return: None
    """
    memory = Memory()
    memory[i] = 0xA5
    assert memory[i] == 0xA5
