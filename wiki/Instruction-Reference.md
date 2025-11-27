# Instruction Reference

## ADC - Add with Carry

A,Z,C,N = A+M+C

This instruction adds the contents of a memory location to the accumulator
together with the carry bit. If overflow occurs the carry bit is set, this
enables multiple byte addition to be performed.

Processor Status after use:

| Flag | Description       | State                        |
| ---- | ----------------- | ---------------------------- |
|  C   | Carry Flag        | Set if overflow in bit 7     |
|  Z   | Zero Flag         | Set if A = 0                 |
|  I   | Interrupt Disable | Not affected                 |
|  D   | Decimal Mode Flag | Not affected                 |
|  B   | Break Command     | Not affected                 |
|  V   | Overflow Flag     | Set if sign bit is incorrect |
|  N   | Negative Flag     | Set if bit 7 set             |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | ------ | ----- | ------------------------ |
| Immediate       |  0x69  |   2   |   2                      |
| Zero Page       |  0x65  |   2   |   3                      |
| Zero Page,X     |  0x75  |   2   |   4                      |
| Absolute        |  0x6D  |   3   |   4                      |
| Absolute,X      |  0x7D  |   3   |   4 (+1 if page crossed) |
| Absolute,Y      |  0x79  |   3   |   4 (+1 if page crossed) |
| (Indirect,X)    |  0x61  |   2   |   6                      |
| (Indirect),Y    |  0x71  |   2   |   5 (+1 if page crossed) |

See also: SBC

## AND - Logical AND

A,Z,N = A&M

A logical AND is performed, bit by bit, on the accumulator contents using
the contents of a byte of memory

Processor Status after use:

| Flag | Description       | State            |
| ---- | ----------------- | ---------------- |
|  C   | Carry Flag        | Not affected     |
|  Z   | Zero Flag         | Set if A = 0     |
|  I   | Interrupt Disable | Not affected     |
|  D   | Decimal Mode Flag | Not affected     |
|  B   | Break Command     | Not affected     |
|  V   | Overflow Flag     | Not affected     |
|  N   | Negative Flag     | Set if bit 7 set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | ------ | ----- | ------------------------ |
| Immediate       |  0x29  |   2   |   2                      |
| Zero Page       |  0x25  |   2   |   3                      |
| Zero Page,X     |  0x35  |   2   |   4                      |
| Absolute        |  0x2D  |   3   |   4                      |
| Absolute,X      |  0x3D  |   3   |   4 (+1 if page crossed) |
| Absolute,Y      |  0x39  |   3   |   4 (+1 if page crossed) |
| (Indirect,X)    |  0x21  |   2   |   6                      |
| (Indirect),Y    |  0x31  |   2   |   5 (+1 if page crossed) |

See also: EOR, ORA

## ASL - Arithmetic Shift Left

ASL - Arithmetic Shift Left.

A,Z,C,N = A*2 or M,Z,C,N = M*2

This instruction adds the contents of a memory location to the accumulator
together with the carry bit. If overflow occurs the carry bit is set, this
enables multiple byte addition to be performed.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Set to contents of old bit 7      |
|  Z   | Zero Flag         | Set if A = 0                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Set if bit 7 of the result is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Accumulator     |  0x0A  |   1   |   2    |
| Zero Page       |  0x06  |   2   |   5    |
| Zero Page,X     |  0x16  |   2   |   6    |
| Absolute        |  0x0E  |   3   |   6    |
| Absolute,X      |  0x1E  |   3   |   7    |

See also: LSR, ROL, ROR

## BCC - Branch if Carry Clear

BCS - Branch if Carry Set.

If the carry flag is clear then add the relative displacement to the program
to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0x90  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BCS

## BCS - Branch if Carry Set

BCS - Branch if Carry Set.

If the carry flag is set then add the relative displacement to the program
to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0xB0  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BCC

## BEQ - Branch if Equal

BEQ - Branch if Equal.

If the zero flag is set then add the relative displacement to the program
to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0xF0  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BNE

## BIT - Bit Test

BIT - Bit Test.

A & M, N = M7, V = M6

This instructions is used to test if one or more bits are set in a target
memory location. The mask pattern in A is ANDed with the value in memory to
set or clear the zero flag, but the result is not kept. Bits 7 and 6 of the
value from memory are copied into the N and V flags.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                    |
| --------------- | ------ | ----- | ------------------------- |
| Zero Page       |  0x24  |   2   | 3                         |
| Absolute        |  0x2C  |   3   | 4                         |

## BMI - Branch if Minus

BMI - Branch if Minus.

If the negative flag is set then add the relative displacement to the program
to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0x30  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BPL

## BNE - Branch if Not Equal

BNE - Branch if Not Equal.

If the zero flag is clear then add the relative displacement to the program
to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0xD0  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BEQ

## BPL - Branch if Positive

BPL - Branch if Positive.

If the negative flag is clear then add the relative displacement to the program
to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0x10  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BMI

## BRK - Force Interrupt

BRK - Force Interrupt.

The BRK instruction forces the generation of an interrupt request. The program
counter and processor status are pushed on the stack then the IRQ interrupt at
vector $FFFE/F is loaded into the PC and the break flag in the status set to
one.

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Set to 1                          |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                    |
| --------------- | ------ | ----- | ------------------------- |
| Implied         |  0x00  |   1   |  7                        |

The interpretation of a BRK depends pn the operating system. On the BBC
Microcomputer it is used by language ROMs to signal run time errors but it
could be used for other purposes (e.g. calling operating system functions,
etc.).

## BVC - Branch if Overflow Clear

BVC - Branch if Overflow Clear.

If the overflow flag is clear then add the relative displacement to the program
counter to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0x50  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BVS

## BVS - Branch if Overflow Set

BVS - Branch if Overflow Set.

If the overflow flag is clear then add the relative displacement to the program
counter to cause a branch to a new location.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Not affected                      |
|  Z   | Zero Flag         | Not affected                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Not affected                      |

| Addressing Mode | Opcode | Bytes | Cycles                                        |
| --------------- | ------ | ----- | --------------------------------------------- |
| Relative        |  0x70  |   2   | 2 (+1 if branch succeeds +2 if to a new page) |

See also: BVC

## CLC - Clear Carry Flag

C = 0

Set the carry flag to zero.

Processor status after use:

| Flag | Description       | State        |
| ---- | ----------------- | ------------ |
|  C   | Carry Flag        | Set to 0     |
|  Z   | Zero Flag         | Not affected |
|  I   | Interrupt Disable | Not affected |
|  D   | Decimal Mode Flag | Not affected |
|  B   | Break Command     | Not affected |
|  V   | Overflow Flag     | Not affected |
|  N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Implied         |  0x18  |   1   |   2    |

See also: SEC

## CLD - Clear Decimal Mode

D = 0

Sets the decimal mode flag to zero.

| Flag | Description       | State        |
| ---- | ----------------- | ------------ |
|  C   | Carry Flag        | Not affected |
|  Z   | Zero Flag         | Not affected |
|  I   | Interrupt Disable | Not affected |
|  D   | Decimal Mode Flag | Set to 0     |
|  B   | Break Command     | Not affected |
|  V   | Overflow Flag     | Not affected |
|  N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Implied         |  0xD8  |   1   |   2    |

NB:
The state of the decimal flag is uncertain when the CPU is powered up and it is
not reset when an interrupt is generated. In both cases you should include an
explicit CLD to ensure that the flag is cleared before performing addition or
subtraction.

See also: SED

## CLI - Clear Interrupt Disable

I = 0

Clears the interrupt disable flag allowing normal interrupt requests to be serviced.

| Flag | Description       | State        |
| ---- | ----------------- | ------------ |
|  C   | Carry Flag        | Not affected |
|  Z   | Zero Flag         | Not affected |
|  I   | Interrupt Disable | Set to 0     |
|  D   | Decimal Mode Flag | Not affected |
|  B   | Break Command     | Not affected |
|  V   | Overflow Flag     | Not affected |
|  N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Implied         |  0x58  |   1   |   2    |

See also: SEI

## CLV - Clear Overflow Flag

V = 0

Clears the overflow flag.

| Flag | Description       | State        |
| ---- | ----------------- | ------------ |
|  C   | Carry Flag        | Not affected |
|  Z   | Zero Flag         | Not affected |
|  I   | Interrupt Disable | Not affected |
|  D   | Decimal Mode Flag | Not affected |
|  B   | Break Command     | Not affected |
|  V   | Overflow Flag     | Set to 0     |
|  N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Implied         |  0xB8  |   1   |   2    |

## CMP - Compare

CMP - Compare.

Z,C,N = A-M

This instruction compares the contents of the accumulator with another memory
held value and sets the zero and carry flags as appropriate.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Set if A >= M                     |
|  Z   | Zero Flag         | Set if A = M                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Set if bit 7 of the result is set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | ------ | ----- | ------------------------ |
| Immediate       |  0xC9  |   2   |   2                      |
| Zero Page       |  0xC5  |   2   |   3                      |
| Zero Page,X     |  0xD5  |   2   |   4                      |
| Absolute        |  0xCD  |   3   |   4                      |
| Absolute,X      |  0xDD  |   3   |   4 (+1 if page crossed) |
| Absolute,Y      |  0xD9  |   3   |   4 (+1 if page crossed) |
| (Indirect,X)    |  0xC1  |   2   |   6                      |
| (Indirect),Y    |  0xD1  |   2   |   5 (+1 if page crossed) |

See also: CPX, CPY

## CPX - Compare X Register

CPX - Compare X Register.

Z,C,N = X-M

This instruction compares the contents of the X register with another memory
held value and sets the zero and carry flags as appropriate.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Set if X >= M                     |
|  Z   | Zero Flag         | Set if X = M                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Set if bit 7 of the result is set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | ------ | ----- | ------------------------ |
| Immediate       |  0xE0  |   2   |   2                      |
| Zero Page       |  0xE4  |   2   |   3                      |
| Absolute        |  0xEC  |   3   |   4                      |

See also: CMP, CPY

## CPY - Compare Y Register

CPY - Compare Y Register.

Z,C,N = Y-M

This instruction compares the contents of the Y register with another memory
held value and sets the zero and carry flags as appropriate.

Processor Status after use:

| Flag | Description       | State                             |
| ---- | ----------------- | --------------------------------- |
|  C   | Carry Flag        | Set if Y >= M                     |
|  Z   | Zero Flag         | Set if Y = M                      |
|  I   | Interrupt Disable | Not affected                      |
|  D   | Decimal Mode Flag | Not affected                      |
|  B   | Break Command     | Not affected                      |
|  V   | Overflow Flag     | Not affected                      |
|  N   | Negative Flag     | Set if bit 7 of the result is set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | ------ | ----- | ------------------------ |
| Immediate       |  0xC0  |   2   |   2                      |
| Zero Page       |  0xC4  |   2   |   3                      |
| Absolute        |  0xCC  |   3   |   4                      |

See also: CMP, CPX

## DEC - Decrement Memory

M,Z,N = M-1

Subtracts one from the value held at a specified memory location setting the
zero and negative flags as appropriate.

| Flag | Description       | State                         |
| ---- | ----------------- | ----------------------------- |
|  C   | Carry Flag        | Not affected                  |
|  Z   | Zero Flag         | Set if result is zero         |
|  I   | Interrupt Disable | Not affected                  |
|  D   | Decimal Mode Flag | Not affected                  |
|  B   | Break Command     | Not affected                  |
|  V   | Overflow Flag     | Not affected                  |
|  N   | Negative Flag     | Set if bit 7 of result is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Zero Page       |  0xC6  |   2   |   5    |
| Zero Page, X    |  0xD6  |   2   |   6    |
| Absolute        |  0xCE  |   3   |   6    |
| Absolute, X     |  0xDE  |   3   |   7    |

See also: DEX, DEY

## DEX - Decrement X Register

X,Z,N = X-1

Subtracts one from the X register setting the zero and negative flags as appropriate.

| Flag | Description       | State                    |
| ---- | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if X is zero         |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of X is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Implied         |  0xCA  |   1   |   2    |

See also: DEC, DEY

## DEY - Decrement Y Register

Y,Z,N = Y-1

Subtracts one from the Y register setting the zero and negative flags as appropriate.

| Flag | Description       | State                    |
| ---- | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if Y is zero         |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of Y is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | ------ | ----- | ------ |
| Implied         |  0x88  |   1   |   2    |

See also: DEC, DEX

## EOR - Exclusive OR
