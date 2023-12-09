"""
TAY - Transfer Accumulator to Y.

Y = A

Copies the current contents of the accumulator into the Y register and sets
the zero and negative flags as appropriate.

Processor Status after use:

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

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0xA8  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: TYA
"""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    ("value", "flag_n", "flag_z"), [
        (0x0F, False, False),
        (0x00, False, True),
        (0xF0, True, False),
    ])
def test_cpu_ins_tay_imm(value: int, flag_n: bool, flag_z: bool) -> None:
    """
    Transfer Accumulator, Implied.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = value
    cpu.reg_y = 0x00
    memory[0xFCE2] = 0xA8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_n,
        cpu.flag_z,
        cpu.reg_y,
    ) == (0xFCE3, 0x01FD, 2, flag_n, flag_z, value)
