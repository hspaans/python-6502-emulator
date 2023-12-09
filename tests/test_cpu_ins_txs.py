"""
TXS - Transfer Register X to Stack Pointer.

S = X

Copies the current contents of the X register into the stack register.

Processor Status after use:

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Not affected             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Not affected |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0x9A  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: TSX
"""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    "value", [
        (0x0F),
        (0x00),
        (0xF0),
    ])
def test_cpu_ins_txs_imm(value: int) -> None:
    """
    Transfer Register X to Stack Pointer, Implied.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_x = value
    memory[0xFCE2] = 0x9A
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.memory[cpu.stack_pointer + 1],
    ) == (0xFCE3, 0x01FC, 2, value)
