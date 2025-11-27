"""
STA - Store Accumulator.

M = A

Stores the contents of the accumulator into memory.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Not affected             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Not affected             |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Zero Page       |  0x85  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, X    |  0x95  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0x8D  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute, X     |  0x9D  |   3   |   5                      |
+-----------------+--------+-------+--------------------------+
| Absolute, Y     |  0x99  |   3   |   5                      |
+-----------------+--------+-------+--------------------------+
| (Indirect, X)   |  0x81  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect), Y   |  0x91  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+

See also: STX, STY
"""
import pytest

from m6502 import Memory, Processor


def test_cpu_ins_sta_zp() -> None:
    """
    Store Accumulator, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    memory[0xFCE2] = 0x85
    memory[0xFCE3] = 0xFC
    memory[0xFC] = 0
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[0xFC],
    ) == (0xFCE4, 0x01FD, 3, 0xF0)


@pytest.mark.parametrize(
    ("reg_x", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_sta_zpx(reg_x: int, memory_location: int) -> None:
    """
    Store Accumulator, Zero Page, X.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0x95
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_sta_abs() -> None:
    """
    Store Accumulator, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    memory[0xFCE2] = 0x8D
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_sta_abx() -> None:
    """
    Store Accumulator, Absolute, X.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    cpu.reg_x = 0x01
    memory[0xFCE2] = 0x9D
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_x] = 0x00
    cpu.execute(5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 5, 0xF0)


def test_cpu_ins_sta_aby() -> None:
    """
    Store Accumulator, Absolute, Y.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    cpu.reg_y = 0x01
    memory[0xFCE2] = 0x99
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_y] = 0x00
    cpu.execute(5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 5, 0xF0)


@pytest.mark.parametrize(
    ("reg_x", "mem_low", "mem_high"), [
        (0x04, 0x0084, 0x0085),
        (0xFF, 0x007F, 0x0080),
    ])
def test_cpu_ins_sta_inx(reg_x: int, mem_low: int, mem_high: int) -> None:
    """
    Store Accumulator, Indexed Indirect.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0x81
    memory[0xFCE3] = 0x80
    memory[mem_low] = 0x74
    memory[mem_high] = 0x20
    memory[0x2074] = 0x00
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 6, 0xF0)


def test_cpu_ins_sta_iny() -> None:
    """
    Load Accumulator, Indirect Indexed.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    cpu.reg_y = 0x10
    memory[0xFCE2] = 0x91
    memory[0xFCE3] = 0x86
    memory[0x0086] = 0x28
    memory[0x0087] = 0x40
    memory[0x4038] = 0x00
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 6, 0xF0)
