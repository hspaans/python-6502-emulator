"""
INX - Increment X Register.

X,Z,N = X+1

Adds one to the X register setting the zero and negative flags as appropriate.

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
|  N   | Negative Flag     | Set if bit 7 of X is set |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0xE8  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: INC, INY

"""
import m6502


def test_cpu_ins_inx_imp_1() -> None:
    """
    Increment X Register from -2 to -1.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = -2
    memory[0xFCE2] = 0xE8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_x,
    ) == (0xFCE3, 0x01FD, 2, False, True, -1)


def test_cpu_ins_inx_imp_2() -> None:
    """
    Increment X Register from -1 to 0.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = -1
    memory[0xFCE2] = 0xE8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_x,
    ) == (0xFCE3, 0x01FD, 2, True, False, 0)


def test_cpu_ins_inx_imp_3() -> None:
    """
    Increment X Register from 0 to 1.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = 0
    memory[0xFCE2] = 0xE8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_x,
    ) == (0xFCE3, 0x01FD, 2, False, False, 1)


def test_cpu_ins_inx_imp_4() -> None:
    """
    Increment X Register from 1 to 2.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = 1
    memory[0xFCE2] = 0xE8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_x,
    ) == (0xFCE3, 0x01FD, 2, False, False, 2)
