"""
BRK - Force Interrupt.

The BRK instruction forces the generation of an interrupt request. The program
counter and processor status are pushed on the stack then the IRQ interrupt at
vector $FFFE/F is loaded into the PC and the break flag in the status set to
one.

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
|  B   | Break Command     | Set to 1                          |
+------+-------------------+-----------------------------------+
|  V   | Overflow Flag     | Not affected                      |
+------+-------------------+-----------------------------------+
|  N   | Negative Flag     | Not affected                      |
+------+-------------------+-----------------------------------+

+-----------------+--------+-------+---------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                    |
+=================+========+=======+===========================+
| Implied         |  0x00  |   1   |  7                        |
+-----------------+--------+-------+---------------------------+

The interpretation of a BRK depends pn the operating system. On the BBC
Microcomputer it is used by language ROMs to signal run time errors but it
could be used for other purposes (e.g. calling operating system functions,
etc.).
"""


def test_cpu_ins_brk_rel() -> None:
    assert False  # TODO: implement test
