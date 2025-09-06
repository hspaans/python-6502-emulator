"""Verifies that the processor class works as expected."""

import sys
from random import choice

import pytest

from m6502 import Memory, Processor

# Opcodes for the 6502 processor.
INS_LDA_IMM = 0xA9  # Load Accumulator, Immediate.
INS_LDA_ZP  = 0XA5  # Load Accumulator, Zero Page.
INS_LDA_ZPX = 0XB5  # Load Accumulator, Zero Page, X.
INS_LDA_ABS = 0xAD  # Load Accumulator, Absolute.
INS_LDA_ABX = 0xBD  # Load Accumulator, Absolute, X.
INS_LDA_ABY = 0xB9  # Load Accumulator, Absolute, Y.
INS_LDA_INX = 0xA1  # Load Accumulator, Indexed Indirect.
INS_LDA_INY = 0xB1  # Load Accumulator, Indirect Indexed.

INS_LDX_IMM = 0xA2  # Load X Register, Immediate.
INS_LDX_ZP  = 0xA6  # Load X Register, Zero Page.
INS_LDX_ZPY = 0xB6  # Load X Register, Zero Page, Y.
INS_LDX_ABS = 0xAE  # Load X Register, Absolute.
INS_LDX_ABY = 0xBE  # Load X Register, Absolute, Y.
INS_LDY_IMM = 0xA0  # Load Y Register, Immediate.

INS_LDY_ZP  = 0xA4  # Load Y Register, Zero Page.
INS_LDY_ZPX = 0xB4  # Load Y Register, Zero Page, X.
INS_LDY_ABS = 0xAC  # Load Y Register, Absolute.
INS_LDY_ABX = 0xBC  # Load Y Register, Absolute, X.

INS_STA_ZP  = 0x85  # Store Accumlator, Zero Page.
INS_STA_ZPX = 0x95  # Store Accumlator, Zero Page, X.
INS_STA_ABS = 0x8D  # Store Accumlator, Absolute.
INS_STA_ABX = 0x9D  # Store Accumlator, Absolute, X.
INS_STA_ABY = 0x99  # Store Accumlator, Absolute, Y.
INS_STA_INX = 0x81  # Store Accumlator, Indexed Indirect.
INS_STA_INY = 0x91  # Store Accumlator, Indirect Indexed.

INS_STX_ZP  = 0x86  # Store X Register, Zero Page.
INS_STX_ZPY = 0x96  # Store X Register, Zero Page, Y.
INS_STX_ABS = 0x8E  # Store X Register, Absolute.

INS_STY_ZP  = 0x84  # Store Y Register, Zero Page.
INS_STY_ZPX = 0x94  # Store Y Register, Zero Page, X.
INS_STY_ABS = 0x8C  # Store Y Register, Absolute.

# Values for the 6502 processor with different flags set.
VALUE8_EMPTY     = 0x00
VALUE8_0000_0000 = 0x00  # Z=T, N=F
VALUE8_0000_1111 = 0x0F  # Z=F, N=F
VALUE8_0101_1010 = 0x5A  # Z=F, N=F
VALUE8_1010_0101 = 0xA5  # Z=F, N=T
VALUE8_1111_0000 = 0xF0  # Z=F, N=T
VALUE8_1111_1111 = 0xFF  # Z=F, N=T


def _random_value(value: int) -> int:
    """
    Generate a random value for testing that is not equal to the given value.

    :param int value: Value to avoid in the random selection.
    :rtype: int
    :return: Random value between 0 and 255.
    """
    return choice([i for i in range(0, 255) if i not in [value]])


def _write_word(memory: Memory, address: int, value: int) -> None:
    """
    Write a word to memory at the specified address.

    :param Memory memory: Memory instance to write to.
    :param int address: Address to write the word to.
    :param int value: Value to write as a word.
    """
    if sys.byteorder == "little":
        memory[address] = value & 0xFF
        memory[address + 1] = (value >> 8) & 0xFF
    else:
        memory[address] = (value >> 8) & 0xFF
        memory[address + 1] = value & 0xFF


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
    ) == (Processor.PC_INIT, Processor.SP_INIT, 0, True, False, True)


def test_cpu_read_byte() -> None:
    """
    Verify CPU can read a byte from memory.

    The cost of the read operation is 1 cycle, and the state of the CPU is
    not changed.
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0x0001] = 0xA5
    value = cpu._read_byte(0x0001)  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (Processor.PC_INIT, Processor.SP_INIT, 1, True, False, True, 0xA5)


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
    value = cpu._read_word(0x0001)  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (Processor.PC_INIT, Processor.SP_INIT, 2, True, False, True, 0x5AA5)


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
    cpu._write_byte(0x0001, 0xA5)  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        memory[0x0001],
    ) == (Processor.PC_INIT, Processor.SP_INIT, 1, True, False, True, 0xA5)


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
    cpu._write_word(0x0001, 0x5AA5)  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        memory[0x0001],
        memory[0x0002],
    ) == (Processor.PC_INIT, Processor.SP_INIT, 2, True, False, True, 0xA5, 0x5A)


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
    cpu._write_byte(0x0001, 0xA5)  # noqa: PLW212
    value = cpu._read_byte(0x0001)  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (Processor.PC_INIT, Processor.SP_INIT, 2, True, False, True, 0xA5)


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
    cpu._write_word(0x0001, 0x5AA5)  # noqa: PLW212
    value = cpu._read_word(0x0001)  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (Processor.PC_INIT, Processor.SP_INIT, 4, True, False, True, 0x5AA5)


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
    value = cpu._fetch_byte()  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (Processor.PC_INIT + 1, Processor.SP_INIT, 1, True, False, True, 0xA5)


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
    value = cpu._fetch_word()  # noqa: PLW212
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i,
        value,
    ) == (Processor.PC_INIT + 2, Processor.SP_INIT, 2, True, False, True, 0x5AA5)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "flag_z", "flag_n"), [
        (2, 2, VALUE8_0000_0000, True, False),
        (2, 2, VALUE8_0000_1111, False, False),
        (2, 2, VALUE8_0101_1010, False, False),
        (2, 2, VALUE8_1010_0101, False, True),
        (2, 2, VALUE8_1111_0000, False, True),
        (2, 2, VALUE8_1111_1111, False, True),
    ])
def test_cpu_ins_lda_imm(size: int, cycles: int, value: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xA9) - Load Accumulator, Immediate.

    Load the value stored after the opcode directly into accumulator
    and then evaluate accumulator for flags Zero and Negative.

    Code example:
    ```
    LDA #nn
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 2 bytes and 2 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDA_IMM
    memory[Processor.PC_INIT + 1] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_zp", "flag_z", "flag_n"), [
        (2, 3, VALUE8_0000_0000, 0x80, True, False),
        (2, 3, VALUE8_0000_1111, 0x80, False, False),
        (2, 3, VALUE8_0101_1010, 0x80, False, False),
        (2, 3, VALUE8_1010_0101, 0x80, False, True),
        (2, 3, VALUE8_1111_0000, 0x80, False, True),
        (2, 3, VALUE8_1111_1111, 0x80, False, True),
    ])
def test_cpu_ins_lda_zp(size: int, cycles: int, value: int, memory_zp: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xA5) - Load Accumulator, Zero Page.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a single byte and within the Zero
    Page memory range of 0-255.

    Code example:
    ```
    LDA nn
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 2 bytes and 3 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_zp: Value used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDA_ZP
    memory[Processor.PC_INIT + 1] = memory_zp
    memory[memory_zp] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value,  flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_zp", "flag_z", "flag_n"), [
        (2, 5, VALUE8_0000_0000, 0x00, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0x00, 0x80, False, False),
        (2, 5, VALUE8_0101_1010, 0x00, 0x80, False, False),
        (2, 5, VALUE8_1010_0101, 0x00, 0x80, False, True),
        (2, 5, VALUE8_1111_0000, 0x00, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0x00, 0x80, False, True),

        (2, 5, VALUE8_0000_0000, 0x0F, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0x0F, 0x80, False, False),
        (2, 5, VALUE8_0101_1010, 0x0F, 0x80, False, False),
        (2, 5, VALUE8_1010_0101, 0x0F, 0x80, False, True),
        (2, 5, VALUE8_1111_0000, 0x0F, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0x0F, 0x80, False, True),

        (2, 5, VALUE8_0000_0000, 0xF0, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0xF0, 0x80, False, False),
        (2, 5, VALUE8_0101_1010, 0xF0, 0x80, False, False),
        (2, 5, VALUE8_1010_0101, 0xF0, 0x80, False, True),
        (2, 5, VALUE8_1111_0000, 0xF0, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0xF0, 0x80, False, True),

        (2, 5, VALUE8_0000_0000, 0xFF, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0xFF, 0x80, False, False),
        (2, 5, VALUE8_0101_1010, 0xFF, 0x80, False, False),
        (2, 5, VALUE8_1010_0101, 0xFF, 0x80, False, True),
        (2, 5, VALUE8_1111_0000, 0xFF, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0xFF, 0x80, False, True),
    ])
def test_cpu_ins_lda_zpx(size: int, cycles: int, value: int, reg_x: int, memory_zp: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xB5) - Load Accumulator, Zero Page, X.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a single byte and within the Zero
    Page memory range of 0-255.

    The Zero Page address may not exceed beyond 0xFF and is calculated by
    adding the value of the X register to the memory location specified by
    the instruction. The result is wrapped around to fit within the Zero Page
    memory range (0-255). For example:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    Code example:
    ```
    LDA nn, X
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 2 bytes and 5 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_zp: Value used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_LDA_ZPX
    memory[Processor.PC_INIT + 1] = memory_zp
    memory[(memory_zp + reg_x) & 0xFF] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0xFAFA, True, False),
        (3, 4, VALUE8_0000_1111, 0xFAFA, False, False),
        (3, 4, VALUE8_0101_1010, 0xFAFA, False, False),
        (3, 4, VALUE8_1010_0101, 0xFAFA, False, True),
        (3, 4, VALUE8_1111_0000, 0xFAFA, False, True),
        (3, 4, VALUE8_1111_1111, 0xFAFA, False, True),
        (3, 4, VALUE8_0000_0000, 0xAFAF, True, False),
        (3, 4, VALUE8_0000_1111, 0xAFAF, False, False),
        (3, 4, VALUE8_0101_1010, 0xAFAF, False, False),
        (3, 4, VALUE8_1010_0101, 0xAFAF, False, True),
        (3, 4, VALUE8_1111_0000, 0xAFAF, False, True),
        (3, 4, VALUE8_1111_1111, 0xAFAF, False, True),
    ])
def test_cpu_ins_lda_abs(size: int, cycles: int, value: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xAD) - Load Accumulator, Absolute.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a two-byte address that can range
    from 0x0000 to 0xFFFF.

    Code example:
    ```
    LDA nnnn
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 3 bytes and 4 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDA_ABS
    if sys.byteorder == "little":
        memory[Processor.PC_INIT + 1] = memory_location & 0xFF
        memory[Processor.PC_INIT + 2] = (memory_location >> 8) & 0xFF
    else:
        memory[Processor.PC_INIT + 1] = (memory_location >> 8) & 0xFF
        memory[Processor.PC_INIT + 2] = memory_location & 0xFF
    memory[memory_location] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0x04, 0x8000, True, False),
        (3, 4, VALUE8_0000_1111, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_0101_1010, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_1010_0101, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_0000, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_1111, 0x04, 0x8000, False, True),
        (3, 5, VALUE8_0000_0000, 0x04, 0x80FE, True, False),
        (3, 5, VALUE8_0000_1111, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_0101_1010, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_1010_0101, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_0000, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_1111, 0x04, 0x80FE, False, True),
    ])
def test_cpu_ins_lda_abx(size: int, cycles: int, value: int, reg_x: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xBD) - Load Accumulator, Absolute, X.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a two-byte address that can range
    from 0x0000 to 0xFFFF. The address is calculated by adding the
    value of the X register to the memory location specified by the
    instruction. The result is wrapped around to fit within the memory
    range (0-65535). For example:

    - 0xFF04 + 0x04 => 0xFF08
    - 0xFF04 + 0xFF => 0x0004 (0x010004)

    Code example:
    ```
    LDA nnnn, X
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 3 bytes and 4 (or 5 when a page boundary is crossed) cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the X register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag

    TODO: Add test cases for page boundary crossing if memory_location + reg_x crosses 0xFFFF
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_LDA_ABX
    if sys.byteorder == "little":
        memory[Processor.PC_INIT + 1] = memory_location & 0xFF
        memory[Processor.PC_INIT + 2] = (memory_location >> 8) & 0xFF
    else:
        memory[Processor.PC_INIT + 1] = (memory_location >> 8) & 0xFF
        memory[Processor.PC_INIT + 2] = memory_location & 0xFF
    memory[memory_location + reg_x] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_y", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0x04, 0x8000, True, False),
        (3, 4, VALUE8_0000_1111, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_1111_0000, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_1111, 0x04, 0x8000, False, True),
        (3, 5, VALUE8_0000_0000, 0x04, 0x80FE, True, False),
        (3, 5, VALUE8_0000_1111, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_1111_0000, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_1111, 0x04, 0x80FE, False, True),
    ])
def test_cpu_ins_lda_aby(size: int, cycles: int, value: int, reg_y: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xB9) - Load Accumulator, Absolute, Y.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a two-byte address that can range
    from 0x0000 to 0xFFFF. The address is calculated by adding the
    value of the Y register to the memory location specified by the
    instruction. The result is wrapped around to fit within the memory
    range (0-65535). For example:

    - 0xFF04 + 0x04 => 0xFF08
    - 0xFF04 + 0xFF => 0x0004 (0x010004)

    Code example:
    ```
    LDA nnnn, Y
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 3 bytes and 4 (or 5 when a page boundary is crossed) cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_y: Value of the Y register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag

    TODO: Add test cases for page boundary crossing if memory_location + reg_y crosses 0xFFFF
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_LDA_ABY
    if sys.byteorder == "little":
        memory[Processor.PC_INIT + 1] = memory_location & 0xFF
        memory[Processor.PC_INIT + 2] = (memory_location >> 8) & 0xFF
    else:
        memory[Processor.PC_INIT + 1] = (memory_location >> 8) & 0xFF
        memory[Processor.PC_INIT + 2] = memory_location & 0xFF
    memory[memory_location + reg_y] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_zp", "memory_location", "flag_z", "flag_n"), [
        (2, 6, VALUE8_0000_0000, 0x04, 0x02, 0x8000, True, False),
        (2, 6, VALUE8_0000_1111, 0x04, 0x02, 0x8000, False, False),
        (2, 6, VALUE8_0101_1010, 0x04, 0x02, 0x8000, False, False),
        (2, 6, VALUE8_1010_0101, 0x04, 0x02, 0x8000, False, True),
        (2, 6, VALUE8_1111_0000, 0x04, 0x02, 0x8000, False, True),
        (2, 6, VALUE8_1111_1111, 0x04, 0x02, 0x8000, False, True),
    ])
def test_cpu_ins_lda_inx(size: int, cycles: int, value: int, reg_x: int, memory_zp: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xA1) - Load Accumulator, Indexed Indirect.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a two-byte address that is
    calculated by adding the value of the X register to the memory location
    specified by the instruction. The result is wrapped around to fit within
    the memory range (0-65535). For example:

    - 0x02 + 0x04 => 0x06
    - 0x02 + 0xFF => 0x01 (0x0101)

    ```
    X = $04
    IMM = $02
    [$06] = 00
    [$07] = 80
    A = [$8000]
    ```

    Code example:
    ```
    LDA ($nn, X)
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 2 bytes and 6 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the X register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag

    TODO: Add test cases for page boundary crossing if memory_zp + reg_x crosses 0xFF
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_LDA_INX
    memory[Processor.PC_INIT + 1] = memory_zp
    if sys.byteorder == "little":
        memory[memory_zp + reg_x] = memory_location & 0xFF
        memory[memory_zp + reg_x + 1] = (memory_location >> 8) & 0xFF
    else:
        memory[memory_zp + reg_x] = (memory_location >> 8) & 0xFF
        memory[memory_zp + reg_x + 1] = memory_location & 0xFF
    memory[memory_location] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_y", "memory_zp", "memory_location", "flag_z", "flag_n"), [
        (2, 5, VALUE8_0000_0000, 0x04, 0x02, 0x8000, True, False),
        (2, 5, VALUE8_0000_1111, 0x04, 0x02, 0x8000, False, False),
        (2, 5, VALUE8_1111_0000, 0x04, 0x02, 0x8000, False, True),
        (2, 5, VALUE8_1111_1111, 0x04, 0x02, 0x8000, False, True),
        (2, 6, VALUE8_0000_0000, 0x04, 0x02, 0x80FE, True, False),
        (2, 6, VALUE8_0000_1111, 0x04, 0x02, 0x80FE, False, False),
        (2, 6, VALUE8_1111_0000, 0x04, 0x02, 0x80FE, False, True),
        (2, 6, VALUE8_1111_1111, 0x04, 0x02, 0x80FE, False, True),
    ])
def test_cpu_ins_lda_iny(size: int, cycles: int, value: int, reg_y: int, memory_zp: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xB1) - Load Accumulator, Indirect Indexed.

    Load the value stored at the memory location that is after the opcode
    directly into accumulator and then evaluate accumulator for flags Zero
    and Negative. The memory location is a two-byte address that is
    calculated by adding the value of the Y register to the memory location
    specified by the instruction. The result is wrapped around to fit within
    the memory range (0-65535). For example:

    - 0x02 + 0x04 => 0x06
    - 0x02 + 0xFF => 0x01 (0x0101)

    ```
    Y = $04
    IMM = $02
    [$02] = 00
    [$03] = 80
    A = [$8000 + Y]
    ```

    Code example:
    ```
    LDA ($nn), Y
    ```

    Affected flags:
    - Zero Flag: Set if A = 0
    - Negative Flag: Set if bit 7 of A is set

    The instruction costs 2 bytes and 5 (or 6 when a page boundary is crossed) cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_y: Value of the Y register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = _random_value(value)
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_LDA_INY
    memory[Processor.PC_INIT + 1] = memory_zp
    if sys.byteorder == "little":
        memory[memory_zp] = memory_location & 0xFF
        memory[memory_zp + 1] = (memory_location >> 8) & 0xFF
    else:
        memory[memory_zp] = (memory_location >> 8) & 0xFF
        memory[memory_zp + 1] = memory_location & 0xFF
    memory[memory_location + reg_y] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "flag_z", "flag_n"), [
        (2, 2, VALUE8_0000_0000, True, False),
        (2, 2, VALUE8_0000_1111, False, False),
        (2, 2, VALUE8_0101_1010, False, False),
        (2, 2, VALUE8_1010_0101, False, True),
        (2, 2, VALUE8_1111_0000, False, True),
        (2, 2, VALUE8_1111_1111, False, True),
    ])
def test_cpu_ins_ldx_imm(size: int, cycles: int, value: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDX (0xA2) - Load X Register, Immediate.

    Load the value stored after the opcode directly into X register
    and then evaluate X register for flags Zero and Negative.

    Assembly example:
    ```
    LDX #nn
    ```

    Affected flags:
    - Zero Flag: Set if X = 0
    - Negative Flag: Set if bit 7 of X is set

    The instruction costs 2 bytes and 2 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDX_IMM
    memory[Processor.PC_INIT + 1] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location", "flag_z", "flag_n"), [
        (2, 3, VALUE8_0000_0000, 0x80, True, False),
        (2, 3, VALUE8_0000_1111, 0x80, False, False),
        (2, 3, VALUE8_0101_1010, 0x80, False, False),
        (2, 3, VALUE8_1010_0101, 0x80, False, True),
        (2, 3, VALUE8_1111_0000, 0x80, False, True),
        (2, 3, VALUE8_1111_1111, 0x80, False, True),
    ])
def test_cpu_ins_ldx_zp(size: int, cycles: int, value: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDX (0xA6) - Load X Register, Zero Page.

    Load the value stored at the memory location that is after the opcode
    directly into X register and then evaluate X register for flags Zero
    and Negative. The memory location is a single byte and within the Zero
    Page memory range of 0-255.

    Code example:
    ```
    LDX nn
    ```

    Affected flags:
    - Zero Flag: Set if X = 0
    - Negative Flag: Set if bit 7 of X is set

    The instruction costs 2 bytes and 3 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_zp: Value used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDX_ZP
    memory[Processor.PC_INIT + 1] = memory_location
    memory[memory_location] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_y", "memory_location", "flag_z", "flag_n"), [
        (2, 5, VALUE8_0000_0000, 0x00, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0x00, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0x00, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0x00, 0x80, False, True),
        (2, 5, VALUE8_0000_0000, 0x0F, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0x0F, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0x0F, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0x0F, 0x80, False, True),
        (2, 5, VALUE8_0000_0000, 0xF0, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0xF0, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0xF0, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0xF0, 0x80, False, True),
        (2, 5, VALUE8_0000_0000, 0xFF, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0xFF, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0xFF, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0xFF, 0x80, False, True),
    ])
def test_cpu_ins_ldx_zpy(size: int, cycles: int, value: int, reg_y: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDX (0xB6) - Load X Register, Zero Page, Y.

    Load the value stored at the memory location that is after the opcode
    directly into X register and then evaluate X register for flags Zero
    and Negative. The memory location is a single byte and within the Zero
    Page memory range of 0-255.

    The Zero Page address may not exceed beyond 0xFF:
    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    Code example:
    ```
    LDX nn, Y
    ```

    Affected flags:
    - Zero Flag: Set if X = 0
    - Negative Flag: Set if bit 7 of X is set

    The instruction costs 2 bytes and 5 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_y: Value of the Y register
    :param int memory_location: Memory location used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = _random_value(value)
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_LDX_ZPY
    memory[Processor.PC_INIT + 1] = memory_location
    memory[(memory_location + reg_y) & 0xFF] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
        cpu.flag_z,
        cpu.flag_n
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0xFAFA, True, False),
        (3, 4, VALUE8_0000_1111, 0xFAFA, False, False),
        (3, 4, VALUE8_0101_1010, 0xFAFA, False, False),
        (3, 4, VALUE8_1010_0101, 0xFAFA, False, True),
        (3, 4, VALUE8_1111_0000, 0xFAFA, False, True),
        (3, 4, VALUE8_1111_1111, 0xFAFA, False, True),
        (3, 4, VALUE8_0000_0000, 0xAFAF, True, False),
        (3, 4, VALUE8_0000_1111, 0xAFAF, False, False),
        (3, 4, VALUE8_0101_1010, 0xAFAF, False, False),
        (3, 4, VALUE8_1010_0101, 0xAFAF, False, True),
        (3, 4, VALUE8_1111_0000, 0xAFAF, False, True),
        (3, 4, VALUE8_1111_1111, 0xAFAF, False, True),
    ])
def test_cpu_ins_ldx_abs(size: int, cycles: int, value: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDX (0xAE) - Load X Register, Absolute.

    Load the value stored at the memory location that is after the opcode
    directly into X register and then evaluate X register for flags Zero
    and Negative. The memory location is a two-byte address.

    Code example:
    ```
    LDX nnnn
    ```

    Affected flags:
    - Zero Flag: Set if X = 0
    - Negative Flag: Set if bit 7 of X is set

    The instruction costs 3 bytes and 4 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_location: Memory location used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDX_ABS
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_y", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0x04, 0x8000, True, False),
        (3, 4, VALUE8_0000_1111, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_0101_1010, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_1010_0101, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_0000, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_1111, 0x04, 0x8000, False, True),
        (3, 5, VALUE8_0000_0000, 0x04, 0x80FE, True, False),
        (3, 5, VALUE8_0000_1111, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_0101_1010, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_1010_0101, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_0000, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_1111, 0x04, 0x80FE, False, True),
    ])
def test_cpu_ins_ldx_aby(size: int, cycles: int, value: int, reg_y: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDX (0xBE) - Load X Register, Absolute, Y.

    Load the value stored at the memory location that is after the opcode
    directly into X register and then evaluate X register for flags Zero
    and Negative. The memory location is a two-byte address that can range
    from 0x0000 to 0xFFFF. The address is calculated by adding the
    value of the Y register to the memory location specified by the
    instruction. The result is wrapped around to fit within the memory
    range (0-65535). For example:

    - 0xFF04 + 0x04 => 0xFF08
    - 0xFF04 + 0xFF => 0x0004 (0x010004)

    Code example:
    ```
    LDX nnnn, Y
    ```
    Affected flags:
    - Zero Flag: Set if X = 0
    - Negative Flag: Set if bit 7 of X is set

    The instruction costs 3 bytes and 4 (or 5 when a page boundary is crossed) cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_y: Value of the Y register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = _random_value(value)
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_LDX_ABY
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location + reg_y] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "flag_z", "flag_n"), [
        (2, 2, VALUE8_0000_0000, True, False),
        (2, 2, VALUE8_0000_1111, False, False),
        (2, 2, VALUE8_0101_1010, False, False),
        (2, 2, VALUE8_1010_0101, False, True),
        (2, 2, VALUE8_1111_0000, False, True),
        (2, 2, VALUE8_1111_1111, False, True),
    ])
def test_cpu_ins_ldy_imm(size: int, cycles: int, value: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDT (0xA0) - Load Y Register, Immediate.

    Load the value stored after the opcode directly into Y register
    and then evaluate Y register for flags Zero and Negative.

    Assembly example:
    ```
    LDY #nn
    ```

    Affected flags:
    - Zero Flag: Set if Y = 0
    - Negative Flag: Set if bit 7 of Y is set

    The instruction costs 2 bytes and 2 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDY_IMM
    memory[Processor.PC_INIT + 1] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location", "flag_z", "flag_n"), [
        (2, 3, VALUE8_0000_0000, 0x80, True, False),
        (2, 3, VALUE8_0000_1111, 0x80, False, False),
        (2, 3, VALUE8_1111_0000, 0x80, False, True),
        (2, 3, VALUE8_1111_1111, 0x80, False, True),
    ])
def test_cpu_ins_ldy_zp(size: int, cycles: int, value: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDA (0xA4) - Load Y Register, Zero Page.

    Load the value stored at the memory location that is after the opcode
    directly into Y register and then evaluate Y register for flags Zero
    and Negative. The memory location is a single byte and within the Zero
    Page memory range of 0-255. The Zero Page address may not exceed beyond
    0xFF:
    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    Code example:
    ```
    LDY nn
    ```

    Affected flags:
    - Zero Flag: Set if Y = 0
    - Negative Flag: Set if bit 7 of Y is set

    The instruction costs 2 bytes and 3 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_location: Memory location used for the test
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDY_ZP
    memory[Processor.PC_INIT + 1] = memory_location
    memory[memory_location] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_location", "flag_z", "flag_n"), [
        (2, 5, VALUE8_0000_0000, 0x00, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0x00, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0x00, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0x00, 0x80, False, True),
        (2, 5, VALUE8_0000_0000, 0x0F, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0x0F, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0x0F, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0x0F, 0x80, False, True),
        (2, 5, VALUE8_0000_0000, 0xF0, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0xF0, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0xF0, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0xF0, 0x80, False, True),
        (2, 5, VALUE8_0000_0000, 0xFF, 0x80, True, False),
        (2, 5, VALUE8_0000_1111, 0xFF, 0x80, False, False),
        (2, 5, VALUE8_1111_0000, 0xFF, 0x80, False, True),
        (2, 5, VALUE8_1111_1111, 0xFF, 0x80, False, True),
    ])
def test_cpu_ins_ldy_zpx(size: int, cycles: int, value: int, reg_x: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDY (0xB4) - Load Y Register, Zero Page, X.

    Load the value stored at the memory location that is after the opcode
    directly into Y register and then evaluate Y register for flags Zero
    and Negative. The memory location is a single byte and within the Zero
    Page memory range of 0-255. The address is calculated by adding the
    value of the X register to the memory location specified by the
    instruction. The result is wrapped around to fit within the memory
    range (0-255). For example:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    Code example:
    ```
    LDY nn, X
    ```

    Affected flags:
    - Zero Flag: Set if Y = 0
    - Negative Flag: Set if bit 7 of Y is set

    The instruction costs 2 bytes and 5 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the X register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = _random_value(value)
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_LDY_ZPX
    memory[Processor.PC_INIT + 1] = memory_location
    memory[(memory_location + reg_x) & 0xFF] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
        cpu.flag_z,
        cpu.flag_n
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0xFAFA, True, False),
        (3, 4, VALUE8_0000_1111, 0xFAFA, False, False),
        (3, 4, VALUE8_0101_1010, 0xFAFA, False, False),
        (3, 4, VALUE8_1010_0101, 0xFAFA, False, True),
        (3, 4, VALUE8_1111_0000, 0xFAFA, False, True),
        (3, 4, VALUE8_1111_1111, 0xFAFA, False, True),
        (3, 4, VALUE8_0000_0000, 0xAFAF, True, False),
        (3, 4, VALUE8_0000_1111, 0xAFAF, False, False),
        (3, 4, VALUE8_0101_1010, 0xAFAF, False, False),
        (3, 4, VALUE8_1010_0101, 0xAFAF, False, True),
        (3, 4, VALUE8_1111_0000, 0xAFAF, False, True),
        (3, 4, VALUE8_1111_1111, 0xAFAF, False, True),
    ])
def test_cpu_ins_ldy_abs(size: int, cycles: int, value: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDY (0xAC) - Load Y Register, Absolute.

    Load the value stored at the memory location that is after the opcode
    directly into Y register and then evaluate Y register for flags Zero
    and Negative. The memory location is a two-byte address that can range
    from 0x0000 to 0xFFFF. The address is specified by the instruction.

    Code example:
    ```
    LDY nnnn
    ```

    Affected flags:
    - Zero Flag: Set if Y = 0
    - Negative Flag: Set if bit 7 of Y is set

    The instruction costs 3 bytes and 4 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = _random_value(value)
    memory[Processor.PC_INIT] = INS_LDY_ABS
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_location", "flag_z", "flag_n"), [
        (3, 4, VALUE8_0000_0000, 0x04, 0x8000, True, False),
        (3, 4, VALUE8_0000_1111, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_0101_1010, 0x04, 0x8000, False, False),
        (3, 4, VALUE8_1010_0101, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_0000, 0x04, 0x8000, False, True),
        (3, 4, VALUE8_1111_1111, 0x04, 0x8000, False, True),
        (3, 5, VALUE8_0000_0000, 0x04, 0x80FE, True, False),
        (3, 5, VALUE8_0000_1111, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_0101_1010, 0x04, 0x80FE, False, False),
        (3, 5, VALUE8_1010_0101, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_0000, 0x04, 0x80FE, False, True),
        (3, 5, VALUE8_1111_1111, 0x04, 0x80FE, False, True),
    ])
def test_cpu_ins_ldy_abx(size: int, cycles: int, value: int, reg_x: int, memory_location: int, flag_z: bool, flag_n: bool) -> None:
    """
    LDY (0xBC) - Load Y Register, Absolute, X.

    Load the value stored at the memory location that is after the opcode
    directly into Y register and then evaluate Y register for flags Zero
    and Negative. The memory location is a two-byte address that can range
    from 0x0000 to 0xFFFF. The address is calculated by adding the
    value of the X register to the memory location specified by the
    instruction. The result is wrapped around to fit within the memory
    range (0-65535). For example:
    - 0xFF04 + 0x04 => 0xFF08
    - 0xFF04 + 0xFF => 0x0004 (0x010004)

    Code example:
    ```
    LDY nnnn, X
    ```

    Affected flags:
    - Zero Flag: Set if Y = 0
    - Negative Flag: Set if bit 7 of Y is set

    The instruction costs 3 bytes and 4 (or 5 when a page boundary is crossed) cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the Y register
    :param int memory_location: Memory location to load the value from
    :param bool flag_z: State of the Zero Flag
    :param bool flag_n: State of the Negative Flag
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = _random_value(value)
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_LDY_ABX
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location + reg_x] = value
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
        cpu.flag_z,
        cpu.flag_n,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value, flag_z, flag_n)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location"), [
        (2, 3, VALUE8_0000_0000, 0x80),
        (2, 3, VALUE8_0000_1111, 0x80),
        (2, 3, VALUE8_0101_1010, 0x80),
        (2, 3, VALUE8_1010_0101, 0x80),
        (2, 3, VALUE8_1111_0000, 0x80),
        (2, 3, VALUE8_1111_1111, 0x80),
    ])
def test_cpu_ins_sta_zp(size: int, cycles: int, value: int, memory_location: int) -> None:
    """
    Store Accumulator, Zero Page.

    Store the value of the Accumulator into the memory location that is
    after the opcode. The memory location is a single byte and within the
    Zero Page memory range of 0-255. The Zero Page address may not exceed
    beyond 0xFF:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    Code example:
    ```
    STA nn
    ```

    Affected flags:
    - None

    The instruction costs 2 bytes and 3 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_location: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    memory[Processor.PC_INIT] = INS_STA_ZP
    memory[Processor.PC_INIT + 1] = memory_location
    memory[memory_location] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_zp"), [
        (2, 3, VALUE8_0000_0000, 0x00, 0x80),
        (2, 3, VALUE8_0000_1111, 0x00, 0x80),
        (2, 3, VALUE8_0101_1010, 0x00, 0x80),
        (2, 3, VALUE8_1010_0101, 0x00, 0x80),
        (2, 3, VALUE8_1111_0000, 0x00, 0x80),
        (2, 3, VALUE8_1111_1111, 0x00, 0x80),

        (2, 3, VALUE8_0000_0000, 0x0F, 0x80),
        (2, 3, VALUE8_0000_1111, 0x0F, 0x80),
        (2, 3, VALUE8_0101_1010, 0x0F, 0x80),
        (2, 3, VALUE8_1010_0101, 0x0F, 0x80),
        (2, 3, VALUE8_1111_0000, 0x0F, 0x80),
        (2, 3, VALUE8_1111_1111, 0x0F, 0x80),

        (2, 3, VALUE8_0000_0000, 0xF0, 0x80),
        (2, 3, VALUE8_0000_1111, 0xF0, 0x80),
        (2, 3, VALUE8_0101_1010, 0xF0, 0x80),
        (2, 3, VALUE8_1010_0101, 0xF0, 0x80),
        (2, 3, VALUE8_1111_0000, 0xF0, 0x80),
        (2, 3, VALUE8_1111_1111, 0xF0, 0x80),

        (2, 3, VALUE8_0000_0000, 0xFF, 0x80),
        (2, 3, VALUE8_0000_1111, 0xFF, 0x80),
        (2, 3, VALUE8_0101_1010, 0xFF, 0x80),
        (2, 3, VALUE8_1010_0101, 0xFF, 0x80),
        (2, 3, VALUE8_1111_0000, 0xFF, 0x80),
        (2, 3, VALUE8_1111_1111, 0xFF, 0x80),
    ])
def test_cpu_ins_sta_zpx(size: int, cycles: int, value: int, reg_x: int, memory_zp: int) -> None:
    """
    STA (0x95) - Store Accumulator, Zero Page, X.

    Store the value of the Accumulator into the memory location that is
    after the opcode. The memory location is a single byte and within the
    Zero Page memory range of 0-255. The address is calculated by adding
    the value of the X register to the memory location specified by the

    Affected flags:
    - None

    The instruction costs 2 bytes and 3 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the X register
    :param int memory_zp: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_STA_ZPX
    memory[Processor.PC_INIT + 1] = memory_zp
    memory[(memory_zp + reg_x) & 0xFF] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[(memory_zp + reg_x) & 0xFF],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location"), [
        (3, 4, VALUE8_0000_0000, 0xFAFA),
        (3, 4, VALUE8_0000_1111, 0xFAFA),
        (3, 4, VALUE8_0101_1010, 0xFAFA),
        (3, 4, VALUE8_1010_0101, 0xFAFA),
        (3, 4, VALUE8_1111_0000, 0xFAFA),
        (3, 4, VALUE8_1111_1111, 0xFAFA),
        (3, 4, VALUE8_0000_0000, 0xAFAF),
        (3, 4, VALUE8_0000_1111, 0xAFAF),
        (3, 4, VALUE8_0101_1010, 0xAFAF),
        (3, 4, VALUE8_1010_0101, 0xAFAF),
        (3, 4, VALUE8_1111_0000, 0xAFAF),
        (3, 4, VALUE8_1111_1111, 0xAFAF),
    ])
def test_cpu_ins_sta_abs(size: int, cycles: int, value: int, memory_location: int) -> None:
    """
    STA (0x8D) - Store Accumulator, Absolute.

    Store the value of the Accumulator into the memory location that is
    after the opcode. The memory location is a two-byte address that can
    range from 0x0000 to 0xFFFF. The address is specified by the
    instruction.

    Code example:
    ```
    STA nnnn
    ```

    Affected flags:
    - None

    The instruction costs 3 bytes and 4 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_location: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    memory[Processor.PC_INIT] = INS_STA_ABS
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_location"), [
        (3, 5, VALUE8_0000_0000, 0x04, 0x8000),
        (3, 5, VALUE8_0000_1111, 0x04, 0x8000),
        (3, 5, VALUE8_0101_1010, 0x04, 0x8000),
        (3, 5, VALUE8_1010_0101, 0x04, 0x8000),
        (3, 5, VALUE8_1111_0000, 0x04, 0x8000),
        (3, 5, VALUE8_1111_1111, 0x04, 0x8000),
        (3, 5, VALUE8_0000_0000, 0x04, 0x80FE),
        (3, 5, VALUE8_0000_1111, 0x04, 0x80FE),
        (3, 5, VALUE8_0101_1010, 0x04, 0x80FE),
        (3, 5, VALUE8_1010_0101, 0x04, 0x80FE),
        (3, 5, VALUE8_1111_0000, 0x04, 0x80FE),
        (3, 5, VALUE8_1111_1111, 0x04, 0x80FE),
    ])
def test_cpu_ins_sta_abx(size: int, cycles: int, value: int, reg_x: int, memory_location: int) -> None:
    """
    STA (0x9D) - Store Accumulator, Absolute, X.

    Store the value of the Accumulator into the memory location that is
    after the opcode. The memory location is a two-byte address that can

    Code example:
    ```
    STA nnnn, X
    ```

    Affected flags:
    - None

    The instruction costs 3 bytes and 5 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the X register
    :param int memory_location: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_STA_ABX
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location + cpu.reg_x] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location + cpu.reg_x],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_y", "memory_location"), [
        (3, 5, VALUE8_0000_0000, 0x04, 0x8000),
        (3, 5, VALUE8_0000_1111, 0x04, 0x8000),
        (3, 5, VALUE8_1111_0000, 0x04, 0x8000),
        (3, 5, VALUE8_1111_1111, 0x04, 0x8000),
        (3, 5, VALUE8_0000_0000, 0x04, 0x80FE),
        (3, 5, VALUE8_0000_1111, 0x04, 0x80FE),
        (3, 5, VALUE8_1111_0000, 0x04, 0x80FE),
        (3, 5, VALUE8_1111_1111, 0x04, 0x80FE),
    ])
def test_cpu_ins_sta_aby(size: int, cycles: int, value: int, reg_y: int, memory_location: int) -> None:
    """
    STA (0x99) - Store Accumulator, Absolute, Y.

    Store the value of the Accumulator into the memory location that is
    after the opcode. The memory location is a two-byte address that can
    range from 0x0000 to 0xFFFF. The address is calculated by adding the
    value of the Y register to the memory location specified by the
    instruction. The result is wrapped around to fit within the memory
    range (0-65535). For example:
    - 0xFF04 + 0x04 => 0xFF08
    - 0xFF04 + 0xFF => 0x0004 (0x010004)

    Code example:
    ```
    STA nnnn, Y
    ```

    Affected flags:
    - None

    The instruction costs 3 bytes and 5 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_y: Value of the Y register
    :param int memory_location: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_STA_ABY
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location + reg_y] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location + reg_y],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_x", "memory_zp", "memory_location"), [
        (2, 6, VALUE8_0000_0000, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_0000_1111, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_0101_1010, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_1010_0101, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_1111_0000, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_1111_1111, 0x04, 0x02, 0x8000),
    ])
def test_cpu_ins_sta_inx(size: int, cycles: int, value: int, reg_x: int, memory_zp: int, memory_location: int) -> None:
    """
    STA (0x81) - Store Accumulator, Indexed Indirect.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_x: Value of the X register
    :param int memory_zp: Zero Page memory location
    :param int memory_location: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_STA_INX
    memory[Processor.PC_INIT + 1] = memory_zp
    _write_word(memory, memory_zp + reg_x, memory_location)
    memory[memory_location] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "reg_y", "memory_zp", "memory_location"), [
        (2, 6, VALUE8_0000_0000, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_0000_1111, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_0101_1010, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_1010_0101, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_1111_0000, 0x04, 0x02, 0x8000),
        (2, 6, VALUE8_1111_1111, 0x04, 0x02, 0x8000),
    ])
def test_cpu_ins_sta_iny(size: int, cycles: int, value: int, reg_y: int, memory_zp: int, memory_location: int) -> None:
    """
    STA (0x91) - Store Accumulator, Indirect Indexed.

    ```
    STA nnnn
    ```

    TODO: This test doesn't test the page crossing.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int reg_y: Value of the Y register
    :param int memory_zp: Zero Page memory location
    :param int memory_location: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_STA_INY
    memory[Processor.PC_INIT + 1] = 0x86
    _write_word(memory, memory_zp, memory_location)
    memory[memory_location + reg_y] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_zp"), [
        (2, 3, VALUE8_0000_0000, 0x80),
        (2, 3, VALUE8_0000_1111, 0x80),
        (2, 3, VALUE8_1111_0000, 0x80),
        (2, 3, VALUE8_1111_1111, 0x80),
    ])
def test_cpu_ins_stx_zp(size: int, cycles: int, value: int, memory_zp: int) -> None:
    """
    STX (0x86) - Store X Register, Zero Page.

    Store the value of the X register into the memory location that is
    after the opcode. The memory location is a single byte and within the
    Zero Page memory range of 0-255.

    Code example:
    ```
    STX nn
    ```

    Affected flags:
    - None

    The instruction costs 2 bytes and 3 cycles to complete.

    :param int size: Number of bytes consumed by the stack pointer
    :param int cycles: Number of CPU cycles used
    :param int value: Value used for the test
    :param int memory_zp: Memory location to store the value in
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = value
    memory[Processor.PC_INIT] = INS_STX_ZP
    memory[Processor.PC_INIT + 1] = memory_zp
    memory[memory_zp] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_zp],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("reg_y", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_stx_zpy(reg_y: int, memory_location: int) -> None:
    """
    STX (0x96) - Store X Register, Zero Page, Y.

    The Zero Page address may not exceed beyond 0xFF:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0xF0
    cpu.reg_y = reg_y
    memory[Processor.PC_INIT] = INS_STX_ZPY
    memory[Processor.PC_INIT + 1] = 0x80
    memory[memory_location] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (0xFCE4, Processor.SP_INIT, 4, 0xF0)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location"), [
        (3, 4, VALUE8_0000_0000, 0xFAFA),
        (3, 4, VALUE8_0000_1111, 0xFAFA),
        (3, 4, VALUE8_0101_1010, 0xFAFA),
        (3, 4, VALUE8_1010_0101, 0xFAFA),
        (3, 4, VALUE8_1111_0000, 0xFAFA),
        (3, 4, VALUE8_1111_1111, 0xFAFA),
        (3, 4, VALUE8_0000_0000, 0xAFAF),
        (3, 4, VALUE8_0000_1111, 0xAFAF),
        (3, 4, VALUE8_0101_1010, 0xAFAF),
        (3, 4, VALUE8_1010_0101, 0xAFAF),
        (3, 4, VALUE8_1111_0000, 0xAFAF),
        (3, 4, VALUE8_1111_1111, 0xAFAF),
    ])
def test_cpu_ins_stx_abs(size: int, cycles: int, value: int, memory_location: int) -> None:
    """
    Store X Register, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = value
    memory[Processor.PC_INIT] = INS_STX_ABS
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location"), [
        (2, 3, VALUE8_0000_0000, 0x80),
        (2, 3, VALUE8_0000_1111, 0x80),
        (2, 3, VALUE8_1111_0000, 0x80),
        (2, 3, VALUE8_1111_1111, 0x80),
    ])
def test_cpu_ins_sty_zp(size: int, cycles: int, value: int, memory_location: int) -> None:
    """Store Y Register, Zero Page."""
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = value
    memory[Processor.PC_INIT] = INS_STY_ZP
    memory[Processor.PC_INIT + 1] = memory_location
    memory[memory_location] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)


@pytest.mark.parametrize(
    ("reg_x", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_sty_zpx(reg_x: int, memory_location: int) -> None:
    """Store Y Register, Zero Page, X."""
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0xF0
    cpu.reg_x = reg_x
    memory[Processor.PC_INIT] = INS_STY_ZPX
    memory[Processor.PC_INIT + 1] = 0x80
    memory[memory_location] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (0xFCE4, Processor.SP_INIT, 4, 0xF0)


@pytest.mark.parametrize(
    ("size", "cycles", "value", "memory_location"), [
        (3, 4, VALUE8_0000_0000, 0xFAFA),
        (3, 4, VALUE8_0000_1111, 0xFAFA),
        (3, 4, VALUE8_0101_1010, 0xFAFA),
        (3, 4, VALUE8_1010_0101, 0xFAFA),
        (3, 4, VALUE8_1111_0000, 0xFAFA),
        (3, 4, VALUE8_1111_1111, 0xFAFA),
        (3, 4, VALUE8_0000_0000, 0xAFAF),
        (3, 4, VALUE8_0000_1111, 0xAFAF),
        (3, 4, VALUE8_0101_1010, 0xAFAF),
        (3, 4, VALUE8_1010_0101, 0xAFAF),
        (3, 4, VALUE8_1111_0000, 0xAFAF),
        (3, 4, VALUE8_1111_1111, 0xAFAF),
    ])
def test_cpu_ins_sty_abs(size: int, cycles: int, value: int, memory_location: int) -> None:
    """STY (0x8C) - Store Y Register, Absolute."""
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = value
    memory[Processor.PC_INIT] = INS_STY_ABS
    _write_word(memory, Processor.PC_INIT + 1, memory_location)
    memory[memory_location] = _random_value(value)
    cpu.execute(cycles)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (Processor.PC_INIT + size, Processor.SP_INIT, cycles, value)
