"""
PHP - Push Processor Status.

Pushes a copy of the status flags on to the stack.

Processor Status after use:

+------+-------------------+--------------+
| Flag | Description       | State        |
+======+===================+==============+
|  C   | Carry Flag        | Not affected |
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
| Implied         |  0x08  |   1   |   3    |
+-----------------+--------+-------+--------+

See also: PLP
"""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    ("value", "flag_n", "flag_z"), [
        (0xAC, False, False),
        (0xEC, False, True),
        (0xAE, True, False),
    ])
def test_cpu_ins_php_imp(value: int, flag_n: bool, flag_z: bool) -> None:
    """
    Push Processor Status, Implied.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0x08
    cpu.flag_z = flag_z
    cpu.flag_n = flag_n
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.memory[cpu.stack_pointer + 1],
    ) == (0xFCE3, 0x01FC, 3, value)
