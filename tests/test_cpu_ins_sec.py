"""
SEC - Set Carry Flag.

C = 1

Set the carry flag to one.

+------+-------------------+--------------+
| Flag | Description       | State        |
+======+===================+==============+
|  C   | Carry Flag        | Set to 1     |
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
| Implied         |  0x38  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: CLC
"""
from m6502 import Memory, Processor


def test_cpu_ins_sec_imp() -> None:
    """
    Set Carry Flag.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.flag_c = False
    memory[0xFCE2] = 0x38
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_c,
    ) == (0xFCE3, 0x01FD, 2, True)
