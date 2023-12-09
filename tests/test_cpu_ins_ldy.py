"""
LDY - Load Y Register.

Y,Z,N = M

Loads a byte of memory into the Y register setting the zero and negative
flags as appropriate.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set is Y = 0             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Set if bit 7 of Y is set |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0xA0  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xA4  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, X    |  0xB4  |   2   |   5                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xAC  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute, X     |  0xBC  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: LDA, LDY
"""
import pytest

from m6502 import Memory, Processor


def test_cpu_ins_ldy_imm() -> None:
    """
    Load Y Register, Immediate.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0x00
    memory[0xFCE2] = 0xA0
    memory[0xFCE3] = 0xF0
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (0xFCE4, 0x01FD, 2, 0xF0)


def test_cpu_ins_ldy_zp() -> None:
    """
    Load Y Register, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0x00
    memory[0xFCE2] = 0xA4
    memory[0xFCE3] = 0xFC
    memory[0xFC] = 0xF0
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (0xFCE4, 0x01FD, 3, 0xF0)


@pytest.mark.parametrize(
    ("reg_x", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_ldy_zpx(reg_x: int, memory_location: int) -> None:
    """
    Load Y Register, Zero Page, X.

    The Zero Page address may not exceed beyond 0xFF:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0x00
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0xB4
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_ldy_abs() -> None:
    """
    Load Y Register, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0x00
    memory[0xFCE2] = 0xAC
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_ldy_abx() -> None:
    """
    Load Y Register, Absolute, X.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = 0x00
    cpu.reg_x = 1
    memory[0xFCE2] = 0xBC
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_x] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_y,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)
