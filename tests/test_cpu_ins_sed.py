"""
SED - Set Decimal Flag.

D = 1

Sets the decimal mode flag to one.

+------+-------------------+--------------+
| Flag | Description       | State        |
+======+===================+==============+
|  C   | Carry Flag        | Not affected |
+------+-------------------+--------------+
|  Z   | Zero Flag         | Not affected |
+------+-------------------+--------------+
|  I   | Interrupt Disable | Not affected |
+------+-------------------+--------------+
|  D   | Decimal Mode Flag | Set to 1     |
+------+-------------------+--------------+
|  B   | Break Command     | Not affected |
+------+-------------------+--------------+
|  V   | Overflow Flag     | Not affected |
+------+-------------------+--------------+
|  N   | Negative Flag     | Not affected |
+------+-------------------+--------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0xF8  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: CLD
"""
from m6502 import Memory, Processor


def test_cpu_ins_sed_imp() -> None:
    """
    Set Decimal Mode.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.flag_d = False
    memory[0xFCE2] = 0xF8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_d,
    ) == (0xFCE3, 0x01FD, 2, True)
