"""
AND - Logical AND.

A,Z,N = A&M

A logical AND is performed, bit by bit, on the accumulator contents using
the contents of a byte of memory

Processor Status after use:

+------+-------------------+------------------+
| Flag | Description       | State            |
+======+===================+==================+
|  C   | Carry Flag        | Not affected     |
+------+-------------------+------------------+
|  Z   | Zero Flag         | Set if A = 0     |
+------+-------------------+------------------+
|  I   | Interrupt Disable | Not affected     |
+------+-------------------+------------------+
|  D   | Decimal Mode Flag | Not affected     |
+------+-------------------+------------------+
|  B   | Break Command     | Not affected     |
+------+-------------------+------------------+
|  V   | Overflow Flag     | Not affected     |
+------+-------------------+------------------+
|  N   | Negative Flag     | Set if bit 7 set |
+------+-------------------+------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0x29  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0x25  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page,X     |  0x35  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0x2D  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute,X      |  0x3D  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| Absolute,Y      |  0x39  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| (Indirect,X)    |  0x21  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect),Y    |  0x31  |   2   |   5 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: EOR, ORA
"""
import pytest

from m6502 import Memory, Processor

testdata = [
    (0x0F, 0xF0, False),
    (0xF0, 0x0F, False),
    (0x0F, 0x0F, True),
    (0xF0, 0xF0, True),
]


@pytest.mark.parametrize(
    ("value_a", "value_mem", "result"),
    testdata
)
def test_cpu_ins_and_imm(value_a: int, value_mem: int, result: bool) -> None:
    assert False  # TODO: implement test


@pytest.mark.parametrize(
    ("value_a", "value_mem", "result"),
    testdata
)
def test_cpu_ins_and_zp(value_a: int, value_mem: int, result: bool) -> None:
    assert False  # TODO: implement test


@pytest.mark.parametrize(
    ("value_a", "value_mem", "result"),
    testdata
)
def test_cpu_ins_and_zpx(value_a: int, value_mem: int, result: bool) -> None:
    assert False  # TODO: implement test
