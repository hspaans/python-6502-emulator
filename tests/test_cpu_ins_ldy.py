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
import m6502


def test_cpu_ins_ldy_imm() -> None:
    """
    Load Y Register, Immediate.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = 0
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
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = 0
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


def test_cpu_ins_ldy_zpx() -> None:
    """
    Load Y Register, Zero Page, X.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = 0
    cpu.reg_x = 1
    memory[0xFCE2] = 0xB4
    memory[0xFCE3] = 0xFC
    memory[0xFC + cpu.reg_x] = 0xF0
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
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = 0
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
