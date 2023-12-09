"""
INY - Increment Y Register.

Y,Z,N = Y+1

Adds one to the Y register setting the zero and negative flags as appropriate.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set if Y is zero         |
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
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    ("value", "expected", "flag_z", "flag_n"), [
        (-2, -1, False, True),
        (-1, 0, True, False),
        (0, 1, False, False),
        (1, 2, False, False)
    ])
def test_cpu_ins_iny_imp(value: int, expected: int, flag_z: bool, flag_n: bool) -> None:
    """
    Increment Y Register.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_y = value
    memory[0xFCE2] = 0xC8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        cpu.reg_y,
    ) == (0xFCE3, 0x01FD, 2, flag_z, flag_n, expected)
