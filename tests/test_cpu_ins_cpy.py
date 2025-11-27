"""
CPY - Compare Y Register.

Z,C,N = Y-M

This instruction compares the contents of the Y register with another memory
held value and sets the zero and carry flags as appropriate.

Processor Status after use:

+------+-------------------+-----------------------------------+
| Flag | Description       | State                             |
+======+===================+===================================+
|  C   | Carry Flag        | Set if Y >= M                     |
+------+-------------------+-----------------------------------+
|  Z   | Zero Flag         | Set if Y = M                      |
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

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0xC0  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xC4  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xCC  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+

See also: CMP, CPX
"""


def test_cpu_ins_cpy_imm() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cpy_zp() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cpy_abs() -> None:
    assert False  # TODO: implement test
