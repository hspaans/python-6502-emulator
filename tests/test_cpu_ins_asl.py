"""
ASL - Arithmetic Shift Left.

A,Z,C,N = A*2 or M,Z,C,N = M*2

This instruction adds the contents of a memory location to the accumulator
together with the carry bit. If overflow occurs the carry bit is set, this
enables multiple byte addition to be performed.

Processor Status after use:

+------+-------------------+-----------------------------------+
| Flag | Description       | State                             |
+======+===================+===================================+
|  C   | Carry Flag        | Set to contents of old bit 7      |
+------+-------------------+-----------------------------------+
|  Z   | Zero Flag         | Set if A = 0                      |
+------+-------------------+-----------------------------------+
|  I   | Interrupt Disable | Not affected                      |
+------+-------------------+-----------------------------------+
|  D   | Decimal Mode Flag | Not affected                      |
+------+-------------------+-----------------------------------+
|  B   | Break Command     | Not affected                      |
+------+-------------------+-----------------------------------+
|  V   | Overflow Flag     | Not affected                      |
+------+-------------------+-----------------------------------+
|  N   | Negative Flag     | Set if bit 7 of the result is set |
+------+-------------------+-----------------------------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Accumulator     |  0x0A  |   1   |   2    |
+-----------------+--------+-------+--------+
| Zero Page       |  0x06  |   2   |   5    |
+-----------------+--------+-------+--------+
| Zero Page,X     |  0x16  |   2   |   6    |
+-----------------+--------+-------+--------+
| Absolute        |  0x0E  |   3   |   6    |
+-----------------+-------+-------+---------+
| Absolute,X      |  0x1E  |   3   |   7    |
+-----------------+--------+-------+--------+

See also: LSR, ROL, ROR
"""
import pytest

from m6502 import Memory, Processor


testdata = [
    (0b00000000, 0b00000001, False, False, False),
    (0b00000001, 0b00000010, False, False, False),
    (0b00000010, 0b00000100, False, False, False),
    (0b00000100, 0b00001000, False, False, False),
    (0b00001000, 0b00010000, False, False, False),
    (0b00010000, 0b00100000, False, False, False),
    (0b00100000, 0b01000000, False, False, False),
    (0b01000000, 0b10000000, False, False, False),
    (0b10000000, 0b00000000, True, False, True),
]


@pytest.mark.parametrize(
    ("value_a", "result", "carry", "zero", "negative"),
    testdata
)
def test_asl_acc(value_a: int, result: int, carry: bool, zero: bool, negative: bool) -> None:
    assert False  # TODO: implement test


@pytest.mark.parametrize(
    ("value_a", "result", "carry", "zero", "negative"),
    testdata
)
def test_asl_zp(value_a: int, result: int, carry: bool, zero: bool, negative: bool) -> None:
    assert False  # TODO: implement test


@pytest.mark.parametrize(
    ("value_a", "result", "carry", "zero", "negative"),
    testdata
)
def test_asl_zpx(value_a: int, result: int, carry: bool, zero: bool, negative: bool) -> None:
    assert False  # TODO: implement test


@pytest.mark.parametrize(
    ("value_a", "result", "carry", "zero", "negative"),
    testdata
)
def test_asl_abs(value_a: int, result: int, carry: bool, zero: bool, negative: bool) -> None:
    assert False  # TODO: implement test


@pytest.mark.parametrize(
    ("value_a", "result", "carry", "zero", "negative"),
    testdata
)
def test_asl_absx(value_a: int, result: int, carry: bool, zero: bool, negative: bool) -> None:
    assert False  # TODO: implement test
