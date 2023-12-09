"""
LDX - Load X Register.

X,Z,N = M

Loads a byte of memory into the X register setting the zero and negative
flags as appropriate.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set is X = 0             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Set if bit 7 of X is set |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0xA2  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xA6  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, Y    |  0xB6  |   2   |   5                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xAE  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute, Y     |  0xBE  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: LDA, LDY
"""
import pytest

from m6502 import Memory, Processor


def test_cpu_ins_ldx_imm() -> None:
    """
    Load X Register, Immediate.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0x00
    memory[0xFCE2] = 0xA2
    memory[0xFCE3] = 0xF0
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (0xFCE4, 0x01FD, 2, 0xF0)


def test_cpu_ins_ldx_zp() -> None:
    """
    Load X Register, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0x00
    memory[0xFCE2] = 0xA6
    memory[0xFCE3] = 0xFC
    memory[0xFC] = 0xF0
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (0xFCE4, 0x01FD, 3, 0xF0)


@pytest.mark.parametrize(
    ("reg_y", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_ldx_zpy(reg_y: int, memory_location: int) -> None:
    """
    Load X Register, Zero Page, Y.

    The Zero Page address may not exceed beyond 0xFF:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0x00
    cpu.reg_y = reg_y
    memory[0xFCE2] = 0xB6
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_ldx_abs() -> None:
    """
    Load X Register, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0x00
    memory[0xFCE2] = 0xAE
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_ldx_aby() -> None:
    """
    Load X Register, Absolute, Y.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 0x00
    cpu.reg_y = 1
    memory[0xFCE2] = 0xBE
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_y] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_x,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)
