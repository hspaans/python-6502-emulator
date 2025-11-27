"""
BEQ - Branch if Equal.

If the zero flag is set then add the relative displacement to the program
to cause a branch to a new location.

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
| Relative        |  0xF0  |   2   | 2 (+1 if branch succeeds  |
|                 |        |       | +2 if to a new page)      |
+-----------------+--------+-------+---------------------------+

See also: BNE
"""


def test_cpu_ins_beq_rel() -> None:
    assert False  # TODO: implement test
