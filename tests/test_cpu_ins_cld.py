"""
CLD - Clear Decimal Mode.

D = 0

Sets the decimal mode flag to zero.

+------+-------------------+--------------+
| Flag | Description       | State        |
+======+===================+==============+
|  C   | Carry Flag        | Not affected |
+------+-------------------+--------------+
|  Z   | Zero Flag         | Not affected |
+------+-------------------+--------------+
|  I   | Interrupt Disable | Not affected |
+------+-------------------+--------------+
|  D   | Decimal Mode Flag | Set to 0     |
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
| Implied         |  0xD8  |   1   |   2    |
+-----------------+--------+-------+--------+

NB:
The state of the decimal flag is uncertain when the CPU is powered up and it
is not reset when an interrupt is generated. In both cases you should include
an explicit CLD to ensure that the flag is cleared before performing addition
or subtraction.

See also: SED
"""
from m6502 import Memory, Processor


def test_cpu_ins_cld_imp() -> None:
    """
    Clear Decimal Mode.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.flag_d = True
    memory[0xFCE2] = 0xD8
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_d,
    ) == (0xFCE3, 0x01FD, 2, False)
