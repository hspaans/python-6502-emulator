"""
DEC - Decrement Memory.

M,Z,N = M-1

Subtracts one from the value held at a specified memory location setting the
zero and negative flags as appropriate.

+------+-------------------+-------------------------------+
| Flag | Description       | State                         |
+======+===================+===============================+
|  C   | Carry Flag        | Not affected                  |
+------+-------------------+-------------------------------+
|  Z   | Zero Flag         | Set if result is zero         |
+------+-------------------+-------------------------------+
|  I   | Interrupt Disable | Not affected                  |
+------+-------------------+-------------------------------+
|  D   | Decimal Mode Flag | Not affected                  |
+------+-------------------+-------------------------------+
|  B   | Break Command     | Not affected                  |
+------+-------------------+-------------------------------+
|  V   | Overflow Flag     | Not affected                  |
+------+-------------------+-------------------------------+
|  N   | Negative Flag     | Set if bit 7 of result is set |
+------+-------------------+-------------------------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Zero Page       |  0xC6  |   2   |   5    |
+-----------------+--------+-------+--------+
| Zero Page, X    |  0xD6  |   2   |   6    |
+-----------------+--------+-------+--------+
| Absolute        |  0xCE  |   3   |   6    |
+-----------------+--------+-------+--------+
| Absolute, X     |  0xDE  |   3   |   7    |
+-----------------+--------+-------+--------+

See also: DEX, DEY

"""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    ("value", "expected", "flag_z", "flag_n"), [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_zp(value: int, expected: int, flag_z: bool, flag_n: bool) -> None:
    """
    Decrement Memory, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0xC6
    memory[0xFCE3] = 0xFC
    memory[0xFC] = value
    cpu.execute(5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFC],
    ) == (0xFCE4, 0x01FD, 5, flag_z, flag_n, expected)


@pytest.mark.parametrize(
    ("value", "expected", "flag_z", "flag_n", "reg_x", "memory_location"), [
        (-1, -2, False, True,  0x0F, 0x8F),
        (0, -1, False, True,  0x0F, 0x8F),
        (1,  0, True,  False, 0x0F, 0x8F),
        (2,  1, False, False, 0x0F, 0x8F),
        (-1, -2, False, True,  0xFF, 0x7F),
        (0, -1, False, True,  0xFF, 0x7F),
        (1,  0, True,  False, 0xFF, 0x7F),
        (2,  1, False, False, 0xFF, 0x7F)
    ])
def test_cpu_ins_dec_zpx(value: int, expected: int, flag_z: bool, flag_n: bool, reg_x: int, memory_location: int) -> None:
    """
    Decrement Memory, Zero Page, X.

    The Zero Page address may not exceed beyond 0xFF:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0xD6
    memory[0xFCE3] = 0x80
    memory[memory_location] = value
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[memory_location],
    ) == (0xFCE4, 0x01FD, 6, flag_z, flag_n, expected)


@pytest.mark.parametrize(
    ("value", "expected", "flag_z", "flag_n"), [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_abs(value: int, expected: int, flag_z: bool, flag_n: bool) -> None:
    """
    Decrement Memory, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0xCE
    memory[0xFCE3] = 0xFC
    memory[0xFCE4] = 0xFA
    memory[0xFAFC] = value
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFAFC],
    ) == (0xFCE5, 0x01FD, 6, flag_z, flag_n, expected)


@pytest.mark.parametrize(
    ("value", "expected", "flag_z", "flag_n"), [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_abx(value: int, expected: int, flag_z: bool, flag_n: bool) -> None:
    """
    Decrement Memory, Absolute, X.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = 1
    memory[0xFCE2] = 0xDE
    memory[0xFCE3] = 0xFC
    memory[0xFCE4] = 0xFA
    memory[0xFAFC + cpu.reg_x] = value
    cpu.execute(7)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFAFC + cpu.reg_x],
    ) == (0xFCE5, 0x01FD, 7, flag_z, flag_n, expected)
