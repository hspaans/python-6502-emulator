"""
PLP - Pull Processor Status.

Pulls an 8 bit value frm the stack and into the processor flags. The flags
will take on new states as determined by value pulled.

Processor Status after use:

+------+-------------------+----------------+
| Flag | Description       | State          |
+======+===================+================+
|  C   | Carry Flag        | Set from stack |
+------+-------------------+----------------+
|  Z   | Zero Flag         | Set from stack |
+------+-------------------+----------------+
|  I   | Interrupt Disable | Set from stack |
+------+-------------------+----------------+
|  D   | Decimal Mode Flag | Set from stack |
+------+-------------------+----------------+
|  B   | Break Command     | Set from stack |
+------+-------------------+----------------+
|  V   | Overflow Flag     | Set from stack |
+------+-------------------+----------------+
|  N   | Negative Flag     | Set from stack |
+------+-------------------+----------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0x28  |   1   |   4    |
+-----------------+--------+-------+--------+

See also: PHP
"""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    ("value", "flag_n", "flag_z"), [
        (0xAC, False, False),
        (0xEC, False, True),
        (0xAE, True, False),
    ])
def test_cpu_ins_plp_imp(value: int, flag_n: bool, flag_z: bool) -> None:
    """
    Pull Processor Status.

    :return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.memory[0xFCE2] = 0x28
    cpu.memory[cpu.stack_pointer] = value
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_n,
        cpu.flag_z,
    ) == (0xFCE3, 0x01FE, 4, flag_n, flag_z)
