"""
CMP - Compare.

Z,C,N = A-M

This instruction compares the contents of the accumulator with another memory
held value and sets the zero and carry flags as appropriate.

Processor Status after use:

+------+-------------------+-----------------------------------+
| Flag | Description       | State                             |
+======+===================+===================================+
|  C   | Carry Flag        | Set if A >= M                     |
+------+-------------------+-----------------------------------+
|  Z   | Zero Flag         | Set if A = M                      |
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
| Immediate       |  0xC9  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xC5  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page,X     |  0xD5  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xCD  |   3   |   4                      |
+-----------------+-------+-------+--------------------------+
| Absolute,X      |  0xDD  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| Absolute,Y      |  0xD9  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| (Indirect,X)    |  0xC1  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect),Y    |  0xD1  |   2   |   5 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: CPX, CPY
"""


def test_cpu_ins_cmp_imm() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_zp() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_zpx() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_abs() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_absx() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_absy() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_indx() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cmp_indy() -> None:
    assert False  # TODO: implement test
