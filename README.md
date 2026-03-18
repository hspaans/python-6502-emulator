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

  The overflow flag is set during arithmetic operations if the result has yielded an invalid 2's complement result (e.g. adding two positive numbers and ending up with a negative result: 64 + 64 => -128). It is determined by looking at the carry between bits 6 and 7 and between bit 7 and the carry flag.

* Negative Flag

  The negative flag is set if the result of the last operation has bit 7 set to a one.

### The Instruction Set

#### Load/Store Operations

##### Loading the Accumulator

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if A = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of A is set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | :----: | :---: | ------------------------ |
| Immediate       |  0xA9  |   2   |   2                      |
| Zero Page       |  0xA5  |   2   |   3                      |
| Zero Page, X    |  0xB5  |   2   |   5                      |
| Absolute        |  0xAD  |   3   |   4                      |
| Absolute, X     |  0xBD  |   3   |   4 (+1 if page crossed) |
| Absolute, Y     |  0xB9  |   3   |   4 (+1 if page crossed) |
| (Indirect, X)   |  0xA1  |   2   |   6                      |
| (Indirect), Y   |  0xB1  |   2   |   5 (+1 if page crossed) |

```assembly
LDA #nn
```

```python
    def _ins_lda_imm(self) -> None:
        """
        LDA (0xA9) - Load Accumulator, Immediate.

        Load the value stored after the opcode directly into accumulator
        and then evaluate accumulator for flags Zero and Negative.

        Assembly example:
        ```
        LDA #nn
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 2 bytes and 2 cycles to complete.
        """
        self.reg_a = self._fetch_byte()
        self._evaluate_flags_nz(self.reg_a)
```

##### Loading the X Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if X = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of X is set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | :----: | :---: | ------------------------ |
| Immediate       |  0xA2  |   2   |   2                      |
| Zero Page       |  0xA6  |   2   |   3                      |
| Zero Page, Y    |  0xB6  |   2   |   5                      |
| Absolute        |  0xAE  |   3   |   4                      |
| Absolute, Y     |  0xBE  |   3   |   4 (+1 if page crossed) |

```assembly
LDX #$nn
```

```python
    def _ins_ldx_zp(self) -> None:
        """
        LDX (0xA6) - Load X Register, Zero Page.

        Load the value stored at the memory location that is after the opcode
        directly into register X and then evaluate register X for flags Zero
        and Negative. The memory location is a single byte and within the Zero
        Page memory range of 0-255.

        Assembly example:
        ```
        LDX #$nn
        ```

        Affected flags:
        - Zero Flag: Set if X = 0
        - Negative Flag: Set if bit 7 of X is set

        The instruction costs 2 bytes and 3 cycles to complete.
        """
        self.reg_x = self._read_byte(self._fetch_byte())
        self._evaluate_flags_nz(self.reg_x)
```

##### Loading the Y Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if Y = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of Y is set |

| Addressing Mode | Opcode | Bytes | Cycles                   |
| --------------- | :----: | :---: | ------------------------ |
| Immediate       |  0xA0  |   2   |   2                      |
| Zero Page       |  0xA4  |   2   |   3                      |
| Zero Page, X    |  0xB4  |   2   |   5                      |
| Absolute        |  0xAC  |   3   |   4                      |
| Absolute, X     |  0xBC  |   3   |   4 (+1 if page crossed) |

```assembly
LDY #$nn
```

```python
    def _ins_ldy_zpx(self) -> None:
        """
        LDY (0xB4) - Load Y Register, Zero Page, X.

        Load the value stored at the memory location that is stored after the
        opcode and increased with the value in register X before copied
        directly into register Y and then evaluate register Y for flags Zero
        and Negative. The memory location is a single byte and within the Zero
        Page memory range of 0-255. The value in register X is added to the
        memory location before the value is read. The value in register X is
        used to point to the memory location of the value to be read. The
        memory location is a single byte and within the Zero Page memory range
        of 0-255. The value in register X is added to the memory location
        before the value is read. The value in register X is used to point to
        the memory location of the value to be read. The value in register X is

        Assembly example:
        ```
        LDY nn,X
        ```

        Affected flags:
        - Zero Flag: Set if Y = 0
        - Negative Flag: Set if bit 7 of Y is set

        The instruction costs 2 bytes and 5 cycles to complete.
        """
        self.reg_y = self._read_byte(
            (self._fetch_byte() + self._read_register_x()) & 0xFF
        )
        self._evaluate_flags_nz(self.reg_y)
        self.cycles += 1  # TODO: Why is the extra cycle required?
```

##### Storing the Accumulator

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Not affected             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Not affected             |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | ------ |
| Zero Page       |  0x85  |   2   |  3     |
| Zero Page, X    |  0x95  |   2   |  4     |
| Absolute        |  0x8D  |   3   |  4     |
| Absolute, X     |  0x9D  |   3   |  5     |
| Absolute, Y     |  0x99  |   3   |  5     |
| (Indirect, X)   |  0x81  |   2   |  6     |
| (Indirect), Y   |  0x91  |   2   |  6     |

```assembly
STA #$nn
```

```python
    def _ins_sta_zpx(self) -> None:
        """
        STA (0x95) - Store Accumulator, Zero Page, X.

        Store the value in the accumulator at the memory location that is
        stored after the opcode and increased with the value in register X. The
        memory location is a single byte and within the Zero Page memory range
        of 0-255. The value in the accumulator is written to the memory
        location without any modification.

        Assembly example:
        ```
        STA nn,X
        ```

        Affected flags:
        - None

        The instruction costs 2 bytes and 4 cycles to complete.
        """
        self._write_byte((self._fetch_byte() + self.reg_x) & 0xFF, self.reg_a)
```

##### Storing the X Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Not affected             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Not affected             |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | ------ |
| Zero Page       |  0x86  |   2   |   3    |
| Zero Page, Y    |  0x96  |   2   |   4    |
| Absolute        |  0x8E  |   3   |   4    |

```assembly
STX #$nn
```

```python
    def _ins_stx_zpy(self) -> None:
        """
        STX (0x96) - Store X Register, Zero Page, Y.

        Store the value in register X at the memory location that is stored
        after the opcode and increased with the value in register Y. The memory
        location is a single byte and within the Zero Page memory range of
        0-255. The value in register Y is added to the memory location before
        the value is read. The value in register Y is used to point to the
        memory location of the value to be read. The memory location is a
        single byte and within the Zero Page memory range of 0-255. The value
        in register Y is added to the memory location before the value is read.
        The value in register Y is used to point to the memory location of the
        value to be read. The value in register Y is added to the memory
        location before the value is read. The value in register Y is used to
        point to the memory location of the value to be read.

        Assembly example:
        ```
        STX (nn),Y
        ```

        Affected flags:
        - None

        The instruction costs 2 bytes and 5 cycles to complete.
        """
        self._write_byte(
            (self._fetch_byte() + self._read_register_y()) & 0xFF, self.reg_x
        )
```

##### Storing the Y Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Not affected             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Not affected             |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Zero Page       |  0x84  |   2   |   3    |
| Zero Page, X    |  0x94  |   2   |   4    |
| Absolute        |  0x8C  |   3   |   4    |

```assembly
STY #$nn
```

```python
    def _ins_sty_zpx(self) -> None:
        """
        STY (0x94) - Store Y Register, Zero Page, X.

        Store the value in register Y at the memory location that is stored
        after the opcode and increased with the value in register X. The memory
        location is a single byte and within the Zero Page memory range of
        0-255. The value in register X is added to the memory location before
        the value is read. The value in register X is used to point to the
        memory location of the value to be read. The memory location is a single
        byte and within the Zero Page memory range of 0-255. The value in
        register X is added to the memory location before the value is read. The
        value in register X is used to point to the memory location of the value
        to be read. The value in register X is added to the memory location
        before the value is read. The value in register X is used to point to
        the memory location of the value to be read.

        Assembly example:
        ```
        STY (nn),X
        ```

        Affected flags:
        - None

        The instruction costs 2 bytes and 5 cycles to complete.
        """
        self._write_byte(
            (self._fetch_byte() + self._read_register_x()) & 0xFF, self.reg_y
        )
```

#### Register Transfer Operations

##### TAX — Transfer Accumulator to X Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if X = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of X is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xAA  |   1   |   2    |

Example:

```asm
    ; Copy the accumulator into X
    LDA #$42   ; A = $42
    TAX        ; X = $42, Z and N set from X
```

##### TAY — Transfer Accumulator to Y Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if Y = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of Y is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xA8  |   1   |   2    |

##### Transfer X Register to Accumulator

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if A = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of A is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x8A  |   1   |   2    |

##### Transfer Y Register to Accumulator

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if A = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of A is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x98  |   1   |   2    |

#### Stack Operations

##### Transfer Stack Pointer to X Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if X = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of X is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xBA  |   1   |   2    |

##### Transfer X Register to Stack Pointer

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Not affected             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Not affected             |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x9A  |   1   |   2    |

##### Push Accumulator to Stack

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Not affected             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Not affected             |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x48  |   1   |   3    |

##### Push processor status to Stack

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Not affected             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Not affected             |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x08  |   1   |   3    |

##### Pull Accumulator from Stack

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if A = 0             |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of A is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x68  |   1   |   4    |

##### Pull processor status from Stack

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Set to value from stack  |
|  Z   | Zero Flag         | Set to value from stack  |
|  I   | Interrupt Disable | Set to value from stack  |
|  D   | Decimal Mode Flag | Set to value from stack  |
|  B   | Break Command     | Set to value from stack  |
|  V   | Overflow Flag     | Set to value from stack  |
|  N   | Negative Flag     | Set to value from stack  |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0x28  |   1   |   4    |

#### Logical Operations

#### Arithmetic Operations

#### Increment/Decrement Operations

##### INC - Increment Memory

| Flag | Description       | State                         |
| :--: | ----------------- | ----------------------------- |
|  C   | Carry Flag        | Not affected                  |
|  Z   | Zero Flag         | Set if result is zero         |
|  I   | Interrupt Disable | Not affected                  |
|  D   | Decimal Mode Flag | Not affected                  |
|  B   | Break Command     | Not affected                  |
|  V   | Overflow Flag     | Not affected                  |
|  N   | Negative Flag     | Set if bit 7 of result is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | ------ |
| Zero Page       |  0xE6  |   2   |   5    |
| Zero Page, X    |  0xF6  |   2   |   6    |
| Absolute        |  0xEE  |   3   |   6    |
| Absolute, X     |  0xFE  |   3   |   7    |

```assembly
INC #$nn
```

##### INX - Increment X Register

| Flag | Description       | State                    |
| :--: | ----------------- | ----------------------- |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if X is zero         |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of X is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | ------ |
| Implied         |  0xE8  |   1   |   2    |

##### INY - Increment Y Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if Y is zero         |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of Y is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xC8  |   1   |   2    |

##### DEC - Decrement Memory

| Flag | Description       | State                         |
| :--: | ----------------- | ----------------------------- |
|  C   | Carry Flag        | Not affected                  |
|  Z   | Zero Flag         | Set if result is zero         |
|  I   | Interrupt Disable | Not affected                  |
|  D   | Decimal Mode Flag | Not affected                  |
|  B   | Break Command     | Not affected                  |
|  V   | Overflow Flag     | Not affected                  |
|  N   | Negative Flag     | Set if bit 7 of result is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Zero Page       |  0xC6  |   2   |   5    |
| Zero Page, X    |  0xD6  |   2   |   6    |
| Absolute        |  0xCE  |   3   |   6    |
| Absolute, X     |  0xDE  |   3   |   7    |

##### DEX - Decrement X Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if X is zero         |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of X is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xCA  |   1   |   2    |

##### DEY - Decrement Y Register

| Flag | Description       | State                    |
| :--: | ----------------- | ------------------------ |
|  C   | Carry Flag        | Not affected             |
|  Z   | Zero Flag         | Set if Y is zero         |
|  I   | Interrupt Disable | Not affected             |
|  D   | Decimal Mode Flag | Not affected             |
|  B   | Break Command     | Not affected             |
|  V   | Overflow Flag     | Not affected             |
|  N   | Negative Flag     | Set if bit 7 of Y is set |

| Addressing Mode | Opcode | Bytes | Cycles |
| --------------- | :----: | :---: | :----: |
| Implied         |  0xC8  |   1   |   2    |

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

#### Implicit Addressing Mode

#### Accumulator Addressing Mode

#### Immediate Addressing Mode

#### Zero Page Addressing Mode

#### Zero Page,X or Zero Page,Y Addressing Mode

#### Relative Addressing Mode

#### Absolute Addressing Mode

#### Absolute,X or Absolute,Y Addressing Mode

#### Indirect Addressing Mode

#### Indirect Indexed Addressing Mode

### The memory model

## The basic structure of a 6502 processor

## Implementing the Set and Clear instructions

[6502]: https://en.m.wikipedia.org/wiki/6502
[Python]: https://www.python.org/
[Raspberry Pi]: https://www.raspberrypi.org/
