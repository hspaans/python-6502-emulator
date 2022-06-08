"""
LDA - Load Accumulator.

A,Z,N = M

Loads a byte of memory into the accumulator setting the zero and negative
flags as appropriate.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set is A = 0             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Set if bit 7 of A is set |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0xA9  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xA5  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, X    |  0xB5  |   2   |   5                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xAD  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute, X     |  0xBD  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| Absolute, Y     |  0xB9  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| (Indirect, X)   |  0xA1  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect), Y   |  0xB1  |   2   |   5 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: LDX, LDY
"""
import m6502


def test_cpu_ins_lda_imm() -> None:
    """
    Load Accumulator, Immediate.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0
    memory[0xFCE2] = 0xA9
    memory[0xFCE3] = 0xF0
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 2, 0xF0)


def test_cpu_ins_lda_zp() -> None:
    """
    Load Accumulator, Zero Page.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0
    memory[0xFCE2] = 0xA5
    memory[0xFCE3] = 0xFC
    memory[0xFC] = 0xF0
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 3, 0xF0)


def test_cpu_ins_lda_zpx() -> None:
    """
    Load Accumulator, Zero Page, X.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0
    cpu.reg_x = 1
    memory[0xFCE2] = 0xB5
    memory[0xFCE3] = 0xFC
    memory[0xFC + cpu.reg_x] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_lda_abs() -> None:
    """
    Load Accumulator, Absolute.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0
    memory[0xFCE2] = 0xAD
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_lda_abx() -> None:
    """
    Load Accumulator, Absolute, X.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0
    cpu.reg_x = 1
    memory[0xFCE2] = 0xBD
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_x] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_lda_aby() -> None:
    """
    Load Accumulator, Absolute, Y.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0
    cpu.reg_y = 1
    memory[0xFCE2] = 0xB9
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_y] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)
