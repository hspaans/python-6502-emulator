"""
INY - Increment Y Register.

Y,Z,N = Y+1

Adds one to the Y register setting the zero and negative flags as appropriate.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set if X is zero         |
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

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0xC8  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: INC, INX

"""
import m6502


def test_cpu_ins_cld_iny_1() -> None:
    """
    Increment Y Register from -2 to -1.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = -2
    memory[0xFCE2] = 0xC8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_y,
    ) == (0xFCE3, 0x01FD, 2, False, True, -1)


def test_cpu_ins_cld_iny_2() -> None:
    """
    Increment Y Register from -1 to 0.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = -1
    memory[0xFCE2] = 0xC8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_y,
    ) == (0xFCE3, 0x01FD, 2, True, False, 0)


def test_cpu_ins_cld_iny_3() -> None:
    """
    Increment Y Register from 0 to 1.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = 0
    memory[0xFCE2] = 0xC8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_y,
    ) == (0xFCE3, 0x01FD, 2, False, False, 1)


def test_cpu_ins_cld_iny_4() -> None:
    """
    Increment Y Register from 1 to 2.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_y = 1
    memory[0xFCE2] = 0xC8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_y,
    ) == (0xFCE3, 0x01FD, 2, False, False, 2)
