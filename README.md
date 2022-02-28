# CS: Writing a 6502 emulator in Python

[Python] is a great language to learn because it is easy to learn and safe to write in. It is also available for Windows, Linux and Mac, and it is free. It is also available on [Raspberry Pi][Raspberry Pi] which is targetted for education and testing purposes. This makes computer science easy accessible to everyone. Also for writing a basic emulator to learn how computers work and what they do. The [6502][6502] processor has a very simple design and a small instruction set that makes it easy to learn.

Learning how processors work also gives the possibility to understand why certain applications are so slow and how to optimize them, but also how to start doing security research by writing a fuzzer to find vulnerabilities. Lets start with the basics and write a simple 6502 emulator before we start with the assembly language.

The [Introduction](#introduction) chapter is mainly based on the **6502 Instruction Set Guide** by [Andrew John Jacobs aka BitWise](https://github.com/andrew-jacobs) and full credit goes to him. Sadly he passed away in 2021 and I copied his work as a reference as his website is no longer available.

## Introduction

### The 6502 basic processor?

### The Registers

#### Program Counter

#### Stack Pointer

#### Accumulator

#### Index registers X and Y

#### Processor Status

As instructions are executed a set of processor flags are set or clear to record the results of the operation. This flags and some additional control flags are held in a special status register. Each flag has a single bit within the register.

Instructions exist to test the values of the various bits, to set or clear some of them and to push or pull the entire set to or from the stack.

* Carry Flag

  The carry flag is set if the last operation caused an overflow from bit 7 of the result or an underflow from bit 0. This condition is set during arithmetic, comparison and during logical shifts. It can be explicitly set using the ['Set Carry Flag' (SEC)](#set-carry-flag) instruction and cleared with ['Clear Carry Flag' (CLC)](#clear-carry-flag).

* Zero Flag

  The zero flag is set of the result of the last operation as was zero.

* Interrupt Disable

  The interrupt disable flag is set if the program has executed a ['Set Interrupt Disable' (SEI)](#sei---set-interrupt-disable) instruction. While this flag is set the processor will not respond to interrupts from devices until it is cleared by a ['Clear Interrupt Disable' (CLI)](#cli---clear-interrupt-disable) instruction.

* Decimal Mode

  While the decimal mode flag is set the processor will obey the rules of Binary Coded Decimal (BCD) arithmetic during addition and subtraction. The flag can be explicitly set using ['Set Decimal Mode' (SED)](#sed---set-decimal-mode) and cleared with ['Clear Decimal Mode' (CLD)](#cld---clear-decimal-mode).
  > Note that only two instructions are affected by the D flag: ['Add with Carry' (ADC)](#adc---add-with-carry) and ['Subtract with Carry' (SBC)](#sbc---subtract-with-carry).

* Break Command

  The break command bit is set when a [BRK](#brk) instruction has been executed and an interrupt has been generated to process it.

* Overflow Flag

  The overflow flag is set during arithmetic operations if the result has yielded an ivalid 2's complement result (e.g. adding to positive numbers an dending up with a negative result: 64 + 64 => -128) It is determined by looking at the carry between bits 6 and 7 and between bit 7 and the carry flag.

* Negative Flag

  The negative flag is set if the result of the last operation has bit 7 set to a one.

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

Set the carry flag to zero.

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

See also [SEC](#sec---set-carry-flag).

##### CLD - Clear Decimal Mode

Sets the decimal mode flag to zero.

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

> The state of the decimal flag is uncertain when the CPU is powered up and it
> is not reset when an interrupt is generated. In both cases you should include
> an explicit CLD to ensure that the flag is cleared before performing addition
> or subtraction.

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
