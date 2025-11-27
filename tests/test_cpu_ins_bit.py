"""
BIT - Bit Test.

A & M, N = M7, V = M6

This instructions is used to test if one or more bits are set in a target
memory location. The mask pattern in A is ANDed with the value in memory to
set or clear the zero flag, but the result is not kept. Bits 7 and 6 of the
value from memory are copied into the N and V flags.

Processor Status after use:

+------+-------------------+-----------------------------------+
| Flag | Description       | State                             |
+======+===================+===================================+
|  C   | Carry Flag        | Not affected                      |
+------+-------------------+-----------------------------------+
|  Z   | Zero Flag         | Not affected                      |
+------+-------------------+-----------------------------------+
|  I   | Interrupt Disable | Not affected                      |
+------+-------------------+-----------------------------------+
|  D   | Decimal Mode Flag | Not affected                      |
+------+-------------------+-----------------------------------+
|  B   | Break Command     | Not affected                      |
+------+-------------------+-----------------------------------+
|  V   | Overflow Flag     | Not affected                      |
+------+-------------------+-----------------------------------+
|  N   | Negative Flag     | Not affected                      |
+------+-------------------+-----------------------------------+

+-----------------+--------+-------+---------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                    |
+=================+========+=======+===========================+
| Zero Page       |  0x24  |   2   | 3                         |
+-----------------+--------+-------+---------------------------+
| Absolute        |  0x2C  |   3   | 4                         |
+-----------------+--------+-------+---------------------------+
"""


def test_cpu_ins_bit_zp() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_bit_abs() -> None:
    assert False  # TODO: implement test
