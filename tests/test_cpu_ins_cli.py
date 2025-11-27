"""
CLI - Clear Interrupt Disable.

I = 0

Clears the interrupt disable flag allowing normal interrupt requests to be
serviced.

+------+-------------------+--------------+
| Flag | Description       | State        |
+======+===================+==============+
|  C   | Carry Flag        | Not affected |
+------+-------------------+--------------+
|  Z   | Zero Flag         | Not affected |
+------+-------------------+--------------+
|  I   | Interrupt Disable | Set to 0     |
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
| Implied         |  0x58  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: SEI
"""
from m6502 import Memory, Processor


def test_cpu_ins_cld_imp() -> None:
    """
    Clear Interrupt Disable.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.flag_i = True
    memory[0xFCE2] = 0x58
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_i,
    ) == (0xFCE3, 0x01FD, 2, False)
