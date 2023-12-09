"""
LDA - Load Accumulator.

A,Z,N = M

Loads a byte of memory into the accumulator setting the zero and negative
flags as appropriate.

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set is A = 0             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Set if bit 7 of A is set |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0xA9  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xA5  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page, X    |  0xB5  |   2   |   5                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xAD  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute, X     |  0xBD  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| Absolute, Y     |  0xB9  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| (Indirect, X)   |  0xA1  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect), Y   |  0xB1  |   2   |   5 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: LDX, LDY
"""
import pytest

from m6502 import Memory, Processor


def test_cpu_ins_lda_imm() -> None:
    """
    Load Accumulator, Immediate.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    memory[0xFCE2] = 0xA9
    memory[0xFCE3] = 0xF0
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 2, 0xF0)


def test_cpu_ins_lda_zp() -> None:
    """
    Load Accumulator, Zero Page.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    memory[0xFCE2] = 0xA5
    memory[0xFCE3] = 0x80
    memory[0x80] = 0xF0
    cpu.execute(3)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 3, 0xF0)


@pytest.mark.parametrize(
    ("reg_x", "memory_location"), [
        (0x0F, 0x8F),
        (0xFF, 0x7F),
    ])
def test_cpu_ins_lda_zpx(reg_x: int, memory_location: int) -> None:
    """
    Load Accumulator, Zero Page, X.

    The Zero Page address may not exceed beyond 0xFF:

    - 0x80 + 0x0F => 0x8F
    - 0x80 + 0xFF => 0x7F (0x017F)

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0xB5
    memory[0xFCE3] = 0x80
    memory[memory_location] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 4, 0xF0)


def test_cpu_ins_lda_abs() -> None:
    """
    Load Accumulator, Absolute.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    memory[0xFCE2] = 0xAD
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_lda_abx() -> None:
    """
    Load Accumulator, Absolute, X.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    cpu.reg_x = 0x01
    memory[0xFCE2] = 0xBD
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_x] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


def test_cpu_ins_lda_aby() -> None:
    """
    Load Accumulator, Absolute, Y.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    cpu.reg_y = 1
    memory[0xFCE2] = 0xB9
    memory[0xFCE3] = 0xFA
    memory[0xFCE4] = 0xFA
    memory[0xFAFA + cpu.reg_y] = 0xF0
    cpu.execute(4)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE5, 0x01FD, 4, 0xF0)


@pytest.mark.parametrize(
    ("reg_x", "mem_low", "mem_high"), [
        (0x04, 0x0084, 0x0085),
        (0xFF, 0x007F, 0x0080),
    ])
def test_cpu_ins_lda_inx(reg_x: int, mem_low: int, mem_high: int) -> None:
    """
    Load Accumulator, Indexed Indirect.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    cpu.reg_x = reg_x
    memory[0xFCE2] = 0xA1
    memory[0xFCE3] = 0x80
    memory[mem_low] = 0x74
    memory[mem_high] = 0x20
    memory[0x2074] = 0xF0
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 6, 0xF0)


def test_cpu_ins_lda_iny() -> None:
    """
    Load Accumulator, Indirect Indexed.

    TODO: This test doesn't test the page crossing.

    return: None
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    cpu.reg_a = 0x00
    cpu.reg_y = 0x10
    memory[0xFCE2] = 0xB1
    memory[0xFCE3] = 0x86
    memory[0x0086] = 0x28
    memory[0x0087] = 0x40
    memory[0x4038] = 0xF0
    cpu.execute(5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.reg_a,
    ) == (0xFCE4, 0x01FD, 5, 0xF0)
