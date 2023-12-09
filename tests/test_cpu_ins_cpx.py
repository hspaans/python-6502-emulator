"""
CPX - Compare X Register.

Z,C,N = X-M

This instruction compares the contents of the X register with another memory
held value and sets the zero and carry flags as appropriate.

Processor Status after use:

+------+-------------------+-----------------------------------+
| Flag | Description       | State                             |
+======+===================+===================================+
|  C   | Carry Flag        | Set if X >= M                     |
+------+-------------------+-----------------------------------+
|  Z   | Zero Flag         | Set if X = M                      |
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
| Immediate       |  0xE0  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0xE4  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0xEC  |   3   |   4                      |
+-----------------+--------+-------+--------------------------+

See also: CMP, CPY
"""


def test_cpu_ins_cpx_imm() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cpx_zp() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_cpx_abs() -> None:
    assert False  # TODO: implement test
