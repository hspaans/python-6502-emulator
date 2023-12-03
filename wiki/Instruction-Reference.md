# Instruction Reference

## ADC - Add with Carry

## AND - Logical AND

## ASL - Arithmetic Shift Left

## BCC - Branch if Carry Clear

## BCS - Branch if Carry Set

## BEQ - Branch if Equal

## BIT - Bit Test

## BMI - Branch if Minus

## BNE - Branch if Not Equal

## BPL - Branch if Positive

## BRK - Force Interrupt

## BVC - Branch if Overflow Clear

## BVS - Branch if Overflow Set

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
The state of the decimal flag is uncertain when the CPU is powered up and it is not reset when an interrupt is generated. In both cases you should include an explicit CLD to ensure that the flag is cleared before performing addition or subtraction.

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

## CPX - Compare X Register

## CPY - Compare Y Register

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
