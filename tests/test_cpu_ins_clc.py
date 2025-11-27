"""
CLC - Clear Carry Flag.

C = 0

Set the carry flag to zero.

+------+-------------------+--------------+
| Flag | Description       | State        |
+======+===================+==============+
|  C   | Carry Flag        | Set to 0     |
+------+-------------------+--------------+
|  Z   | Zero Flag         | Not affected |
+------+-------------------+--------------+
|  I   | Interrupt Disable | Not affected |
+------+-------------------+--------------+
|  D   | Decimal Mode Flag | Not affected |
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
| Implied         |  0x18  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: SEC
"""
from m6502 import Memory, Processor


def test_cpu_ins_clc_imp() -> None:
    """
    CLC - Clear Carry Flag.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.flag_c = True
    memory[0xFCE2] = 0x18
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_c,
    ) == (0xFCE3, 0x01FD, 2, False)
