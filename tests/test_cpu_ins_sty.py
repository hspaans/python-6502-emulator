"""
STY - Store Y Register.

M = Y

Stores the contents of the Y register into memory.

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
| Zero Page       |  0x84  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, X    |  0x94  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0x8C  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+

See also: STY, STX
"""
import pytest

from m6502 import Memory, Processor


def test_cpu_ins_sty_zp() -> None:
    """
    Store Y Register, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0xF0
    memory[0xFCE2] = 0x84
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
def test_cpu_ins_sty_zpx(reg_x: int, memory_location: int) -> None:
    """
    Store Y Register, Zero Page, X.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0xF0
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0x94
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_sty_abs() -> None:
    """
    Store Y Register, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0xF0
    memory[0xFCE2] = 0x8C
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)
