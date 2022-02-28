# CS: Writing a 6502 emulator in Python

[Python] is a great language to learn because it is easy to learn and safe to write in. It is also available for Windows, Linux and Mac, and it is free. It is also available on [Raspberry Pi][Raspberry Pi] which is targetted for education and testing purposes. This makes computer science easy accessible to everyone. Also for writing a basic emulator to learn how computers work and what they do. The [6502][6502] processor has a very simple design and a small instruction set that makes it easy to learn.

Learning how processors work also gives the possibility to understand why certain applications are so slow and how to optimize them, but also how to start doing security research by writing a fuzzer to find vulnerabilities. Lets start with the basics and write a simple 6502 emulator before we start with the assembly language.

## Introduction

### The 6502 basic processor?

### The Registers

#### Program Counter

#### Stack Pointer

#### Accumulator

#### Index registers X and Y

#### Processor Status

* Carry Flag
* Zero Flag
* Interrupt Disable
* Decimal Mode
* Break Command
* Overflow Flag
* Negative Flag

### The Instruction Set

#### Load/Store Operations

#### Register Transfer Operations

#### Stack Operations

#### Logical Operations

#### Arithmetic Operations

#### Increment/Decrement Operations

#### Bitwise Operations

#### Jump/Call Operations

#### Branch Operations

#### Status Flag Changes

##### CLC - Clear Carry Flag

Set the carry flag to zero. See also [SEC](#sec---set-carry-flag).

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Set to 0     |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Not affected |
|   D   | Decimal Mode Flag | Not affected |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x18  |   1   |   2    |

##### CLD - Clear Decimal Mode

Sets the decimal mode flag to zero.

The state of the decimal flag is uncertain when the CPU is powered up and it
is not reset when an interrupt is generated. In both cases you should include
an explicit CLD to ensure that the flag is cleared before performing addition
or subtraction.

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Not affected |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Not affected |
|   D   | Decimal Mode Flag | Set to 0     |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xD8  |   1   |   2    |

See also [SED](#sed---set-decimal-mode).

##### CLI - Clear Interrupt Disable

Clears the interrupt disable flag allowing normal interrupt requests to be
serviced.

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Not affected |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Set to 0     |
|   D   | Decimal Mode Flag | Not affected |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x58  |   1   |   2    |

See also [SEI](#sei---set-interrupt-disable).

##### CLV - Clear Overflow Flag

Clears the overflow flag.

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Not affected |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Not affected |
|   D   | Decimal Mode Flag | Not affected |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Set to 0     |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xB8  |   1   |   2    |

##### SEC - Set Carry Flag

Set the carry flag to one.

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Set to 1     |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Not affected |
|   D   | Decimal Mode Flag | Not affected |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x38  |   1   |   2    |

See also [CLC](#clc---clear-carry-flag).

##### SED - Set Decimal Mode

Sets the decimal mode flag to one.

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Not affected |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Not affected |
|   D   | Decimal Mode Flag | Set to 1     |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xF8  |   1   |   2    |

See also [CLD](#cld---clear-decimal-mode).

##### SEI - Set Interrupt Disable

Sets the interrupt disable flag to zero.

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Not affected |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Set to 1     |
|   D   | Decimal Mode Flag | Not affected |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x78  |   1   |   2    |

See also [CLI](#cli---clear-interrupt-disable).

#### System Functions

##### NOP - No Operation

The NOP instruction causes no changes to the processor other than the normal
incrementing of the program counter to the next instruction.

Processor Status after use:

| Flag  | Description       | State        |
| :---: | ----------------- | ------------ |
|   C   | Carry Flag        | Not affected |
|   Z   | Zero Flag         | Not affected |
|   I   | Interrupt Disable | Not affected |
|   D   | Decimal Mode Flag | Not affected |
|   B   | Break Command     | Not affected |
|   V   | Overflow Flag     | Not affected |
|   N   | Negative Flag     | Not affected |


| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xEA  |   1   |   2    |

### Addressing Modes

#### Implicit

#### Accumulator

#### Immediate

#### Zero Page

#### Zero Page,X or Zero Page,Y

#### Relative

#### Absolute

#### Absolute,X or Absolute,Y

#### Indirect

#### Indirect Indexed



### The memory model

## The basic structure of a 6502 processor

## Implementing the Set and Clear instructions

[6502]: https://en.m.wikipedia.org/wiki/6502
[Python]: https://www.python.org/
[Raspberry Pi]: https://www.raspberrypi.org/
