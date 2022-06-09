"""
STA - Store Accumulator.

M = A

Stores the contents of the accumulator into memory.

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
|  N   | Negative Flag     | Not affected             |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Zero Page       |  0x85  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, X    |  0x95  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0x8D  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute, X     |  0x9D  |   3   |   5                      |
+-----------------+--------+-------+--------------------------+
| Absolute, Y     |  0x99  |   3   |   5                      |
+-----------------+--------+-------+--------------------------+
| (Indirect, X)   |  0x81  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect), Y   |  0x81  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+

See also: STX, STY
"""
import pytest
import m6502


def test_cpu_ins_sta_zp() -> None:
    """
    Store Accumulator, Zero Page.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    memory[0xFCE2] = 0x85
    memory[0xFCE3] = 0xFC
    memory[0xFC] = 0
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[0xFC],
    ) == (0xFCE4, 0x01FD, 3, 0xF0)


@pytest.mark.parametrize(
    "reg_x, memory_location", [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_sta_zpx(reg_x: int, memory_location: int) -> None:
    """
    Store Accumulator, Zero Page, X.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0x95
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        memory[memory_location],
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_sta_abs() -> None:
    """
    Store Accumulator, Absolute.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_a = 0xF0
    memory[0xFCE2] = 0x8D
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0x00
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)
