"""
ADC - Add with Carry.

A,Z,C,N = A+M+C

This instruction adds the contents of a memory location to the accumulator
together with the carry bit. If overflow occurs the carry bit is set, this
enables multiple byte addition to be performed.

Processor Status after use:

+------+-------------------+------------------------------+
| Flag | Description       | State                        |
+======+===================+==============================+
|  C   | Carry Flag        | Set if overflow in bit 7     |
+------+-------------------+------------------------------+
|  Z   | Zero Flag         | Set if A = 0                 |
+------+-------------------+------------------------------+
|  I   | Interrupt Disable | Not affected                 |
+------+-------------------+------------------------------+
|  D   | Decimal Mode Flag | Not affected                 |
+------+-------------------+------------------------------+
|  B   | Break Command     | Not affected                 |
+------+-------------------+------------------------------+
|  V   | Overflow Flag     | Set if sign bit is incorrect |
+------+-------------------+------------------------------+
|  N   | Negative Flag     | Set if bit 7 set             |
+------+-------------------+------------------------------+

+-----------------+--------+-------+--------------------------+
| Addressing Mode | Opcode | Bytes | Cycles                   |
+=================+========+=======+==========================+
| Immediate       |  0x69  |   2   |   2                      |
+-----------------+--------+-------+--------------------------+
| Zero Page       |  0x65  |   2   |   3                      |
+-----------------+--------+-------+--------------------------+
| Zero Page,X     |  0x75  |   2   |   4                      |
+-----------------+--------+-------+--------------------------+
| Absolute        |  0x6D  |   3   |   4                      |
+-----------------+-------+-------+--------------------------+
| Absolute,X      |  0x7D  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| Absolute,Y      |  0x79  |   3   |   4 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+
| (Indirect,X)    |  0x61  |   2   |   6                      |
+-----------------+--------+-------+--------------------------+
| (Indirect),Y    |  0x71  |   2   |   5 (+1 if page crossed) |
+-----------------+--------+-------+--------------------------+

See also: SBC
"""
import pytest

from m6502 import Memory, Processor


@pytest.mark.parametrize(
    ("value_a", "value_mem", "result"),
    [
        (0x0F, 0xF0, False),
        (0xF0, 0x0F, False),
        (0x0F, 0x0F, True),
        (0xF0, 0xF0, True),
    ]
)
def test_cpu_ins_adc_imm(value_a: int, value_mem: int, result: bool) -> None:
    assert False  # TODO: implement test


def test_cpu_ins_adc_zp() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_adc_zpx() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_adc_abs() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_adc_absx() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_adc_absy() -> None:
    assert False  # TODO: implement test


def test_cpu_ins_adc_indx() -> None:
    assert False  # TODO: implement test
