"""
STX - Store X Register.

M = X

Stores the contents of the X register into memory.

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
| Zero Page       |  0x86  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, Y    |  0x96  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0x8E  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+

See also: STA, STY
"""
import pytest

from m6502 import Memory, Processor


def test_cpu_ins_stx_zp() -> None:
    """
    Store X Register, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0xF0
    memory[0xFCE2] = 0x86
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
    ("reg_y", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_stx_zpy(reg_y: int, memory_location: int) -> None:
    """
    Store X Register, Zero Page, Y.

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
    memory[0xFCE2] = 0x96
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_stx_abs() -> None:
    """
    Store X Register, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0xF0
    memory[0xFCE2] = 0x8E
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)
