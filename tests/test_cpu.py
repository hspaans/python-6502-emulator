"""Verifies that the processor class works as expected."""
from m6502 import Memory, Processor


def test_cpu_reset() -> None:
    """
    Verify CPU state after CPU Reset.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
    ) == (0xFCE2, 0x01FD, 0, True, False, True)


def test_cpu_read_byte() -> None:
    """
    Verify CPU can read a byte from memory.

    The cost of the read operation is 1 cycle, and the state of the CPU is
    not changed.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0x0001] = 0xA5
    value = cpu.read_byte(0x0001)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (0xFCE2, 0x01FD, 1, True, False, True, 0xA5)


def test_cpu_read_word() -> None:
    """
    Verify CPU can read a word from memory.

    The cost of the read operation is 2 cycles, and the state of the CPU is
    not changed.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0x0001] = 0xA5
    memory[0x0002] = 0x5A
    value = cpu.read_word(0x0001)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (0xFCE2, 0x01FD, 2, True, False, True, 0x5AA5)


def test_cpu_write_byte() -> None:
    """
    Verify CPU can write a byte to memory.

    The cost of the write operation is 1 cycle, and the state of the CPU is
    not changed.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.write_byte(0x0001, 0xA5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        memory[0x0001],
    ) == (0xFCE2, 0x01FD, 1, True, False, True, 0xA5)


def test_cpu_write_word() -> None:
    """
    Verify CPU can write a byte to memory.

    The cost of the write operation is 1 cycle, and the state of the CPU is
    not changed.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.write_word(0x0001, 0x5AA5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        memory[0x0001],
        memory[0x0002],
    ) == (0xFCE2, 0x01FD, 2, True, False, True, 0xA5, 0x5A)


def test_cpu_read_write_byte() -> None:
    """
    Verify CPU can read and write a byte from memory.

    The cost of the read operation is 1 cycle, and the state of the CPU is
    not changed.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.write_byte(0x0001, 0xA5)
    value = cpu.read_byte(0x0001)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (0xFCE2, 0x01FD, 2, True, False, True, 0xA5)


def test_cpu_read_write_word() -> None:
    """
    Verify CPU can read and write a byte from memory.

    The cost of the read operation is 1 cycle, and the state of the CPU is
    not changed.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.write_word(0x0001, 0x5AA5)
    value = cpu.read_word(0x0001)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (0xFCE2, 0x01FD, 4, True, False, True, 0x5AA5)


def test_cpu_fetch_byte() -> None:
    """
    Verify CPU can fetch a byte from memory.

    The cost of the fetch operation is 1 cycle, and increases the program
    counter by 1. The state of the CPU is not changed further.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0xA5
    value = cpu.fetch_byte()
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (0xFCE3, 0x01FD, 1, True, False, True, 0xA5)


def test_cpu_fetch_word() -> None:
    """
    Verify CPU can fetch a word from memory.

    The cost of the fetch operation is 2 cycle, and increases the program
    counter by 2. The state of the CPU is not changed further.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0xA5
    memory[0xFCE3] = 0x5A
    value = cpu.fetch_word()
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (0xFCE4, 0x01FD, 2, True, False, True, 0x5AA5)
