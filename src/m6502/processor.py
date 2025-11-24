"""Emulation of the MOT-6502 Processor."""

import sys

from . import Memory


class Processor:  # noqa: PLR904
    """
    MOT-6502 Processor.

    Memory Structure and Special Areas

    The 6502 utilizes a 16-bit address bus, allowing it to address 65536 bytes ($0000-$FFFF). This memory space is conceptually divided into 256 pages, each containing 256 memory locations.

    1. Zero Page ($0000-$00FF): This first page is particularly significant for 6502 addressing. Address modes that operate on the Zero Page are special because they only require an 8-bit operand to specify the address, compared to the 16-bit operand needed for addresses in other pages. This results in shorter instruction sizes (2 bytes vs. 3 bytes) and faster execution (typically one cycle quicker). The Zero Page is often used for variables and constants due to this speed advantage, making it behave somewhat like additional registers. The 65816, a later processor, uses direct addressing modes that add the contents of a direct register to a zeropage address instead of traditional zeropage modes.

    2. Stack ($0100-$01FF): The second page of memory is reserved for the processor stack and cannot be relocated. This is a 256-byte Last-In-First-Out (LIFO) stack, which grows downwards from $01FF towards $0100. The 8-bit Stack Pointer (SP) register holds the low byte (offset) of the current stack address, meaning the actual memory location is $0100 + SP. Pushing a byte stores the value at the current SP location ($0100,S) and then post-decrements the SP. Pulling increments the SP first, then retrieves the byte from the new location.

    3. General-Purpose ($0200-$FFFF): The remaining memory is used for various purposes, including RAM, ROM, and memory-mapped I/O devices. Jump vectors for interrupts and reset are located at the very top of this space, from $FFFA to $FFFF.

    Types of Address Modes

    The 6502 supports various address modes, allowing instructions to obtain their operands or target addresses in different ways. These modes are part of the instruction's opcode pattern and affect the instruction's size and execution time.

    Common address modes include:
      - Impliced
      - Immediate: The operand is a literal 8-bit value provided immediately
        after the opcode in memory. It is typically prefixed with # in assembly syntax. Example: LDA #nn

      - Absolute: The operand is a full 16-bit address pointing to any location
        in the 64KB memory space. Example: LDX nnnn

      - Absolute, X: The operand is a full 16-bit address pointing to any
        location in the 64KB memory space. Example: LDX nnnn,X

      - Absolute, Y:
      - Zero Page: The operand is an 8-bit address pointing to a location in the
        Zero Page ($0000-$00FF). This is faster and uses fewer bytes than
        absolute addressing. Example: LDA nnnn

      - Zero Page, X: LDA

      - Zero Page, Y:

      - Indexed Indirect
      - Indirect Indexed
    """

    PC_INIT = 0xFCE2  # Hardcoded start vector post-reset
    SP_INIT = 0x01FD  # Hardcoded stack pointer post-reset

    # fmt: off
    _ADDRESSING = [
        #  0  |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  A   |  B   |  C   |  D   |  E   |  F   |
        "imp", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "abs", "abs", "abs", "abs",  # 0
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 1
        "abs", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "abs", "abs", "abs", "abs",  # 2
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 3
        "imp", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "abs", "abs", "abs", "abs",  # 4
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 5
        "imp", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "ind", "abs", "abs", "abs",  # 6
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 7
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # 8
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpy", "zpy", "imp", "aby", "imp", "aby", "abx", "abx", "aby", "aby",  # 9
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # A
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpy", "zpy", "imp", "aby", "imp", "aby", "abx", "abx", "aby", "aby",  # B
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # C
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # D
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # E
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # F
    ]

    _OPCODES = [
        #  0  |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  A   |  B   |  C   |  D   |  E   |  F   |
        "brk", "ora", "nop", "slo", "nop", "ora", "asl", "slo", "php", "ora", "asl", "nop", "nop", "ora", "asl", "slo",  # 0
        "bpl", "ora", "nop", "slo", "nop", "ora", "asl", "slo", "clc", "ora", "nop", "slo", "nop", "ora", "asl", "slo",  # 1
        "jsr", "and", "nop", "rla", "bit", "and", "rol", "rla", "plp", "and", "rol", "nop", "bit", "and", "rol", "rla",  # 2
        "bmi", "and", "nop", "rla", "nop", "and", "rol", "rla", "sec", "and", "nop", "rla", "nop", "and", "rol", "rla",  # 3
        "rti", "eor", "nop", "sre", "nop", "eor", "lsr", "sre", "pha", "eor", "lsr", "nop", "jmp", "eor", "lsr", "sre",  # 4
        "bvc", "eor", "nop", "sre", "nop", "eor", "lsr", "sre", "cli", "eor", "nop", "sre", "nop", "eor", "lsr", "sre",  # 5
        "rts", "adc", "nop", "rra", "nop", "adc", "ror", "rra", "pla", "adc", "ror", "nop", "jmp", "adc", "ror", "rra",  # 6
        "bvs", "adc", "nop", "rra", "nop", "adc", "ror", "rra", "sei", "adc", "nop", "rra", "nop", "adc", "ror", "rra",  # 7
        "nop", "sta", "nop", "sax", "sty", "sta", "stx", "sax", "dey", "nop", "txa", "nop", "sty", "sta", "stx", "sax",  # 8
        "bcc", "sta", "nop", "nop", "sty", "sta", "stx", "sax", "tya", "sta", "txs", "nop", "nop", "sta", "nop", "nop",  # 9
        "ldy", "lda", "ldx", "lax", "ldy", "lda", "ldx", "lax", "tay", "lda", "tax", "nop", "ldy", "lda", "ldx", "lax",  # A
        "bcs", "lda", "nop", "lax", "ldy", "lda", "ldx", "lax", "clv", "lda", "tsx", "lax", "ldy", "lda", "ldx", "lax",  # B
        "cpy", "cmp", "nop", "dcp", "cpy", "cmp", "dec", "dcp", "iny", "cmp", "dex", "nop", "cpy", "cmp", "dec", "dcp",  # C
        "bne", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp", "cld", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp",  # D
        "cpx", "sbc", "nop", "isb", "cpx", "sbc", "inc", "isb", "inx", "sbc", "nop", "sbc", "cpx", "sbc", "inc", "isb",  # E
        "beq", "sbc", "nop", "isb", "nop", "sbc", "inc", "isb", "sed", "sbc", "nop", "isb", "nop", "sbc", "inc", "isb",  # F
    ]

    def __init__(self, memory: Memory) -> None:
        """
        Initialize the processor.

        :param memory: The memory to use
        """
        self.memory = memory
        self.reg_a = 0  # Accumulator A
        self.reg_y = 0  # Index Register Y
        self.reg_x = 0  # Index Register X

        self.program_counter = 0  # Program Counter PC
        self.stack_pointer   = 0  # Stack Pointer S
        self.cycles          = 0  # Cycles used

        self.flag_c = True  # Status flag - Carry Flag
        self.flag_z = True  # Status flag - Zero Flag
        self.flag_i = True  # Status flag - Interrupt Disable
        self.flag_d = True  # Status flag - Decimal Mode Flag
        self.flag_b = True  # Status flag - Break Command
        self.flag_v = True  # Status flag - Overflow Flag
        self.flag_n = True  # Status flag - Negative Flag

    def reset(self) -> None:
        """Reset processor to initial state."""
        self.program_counter = self.PC_INIT  # Hardcoded start vector post-reset
        self.stack_pointer   = self.SP_INIT  # Hardcoded stack pointer post-reset
        self.cycles          = 0             # Set cycle count to zero
        self.flag_i          = True          # Set Interrupt Disable to True
        self.flag_d          = False         # Set Decimal Mode to False
        self.flag_b          = True          # Set Break Command to True
    # fmt: on

    def _fetch_byte(self) -> int:
        """
        Fetch a byte from memory[program-counter].

        Fetch a byte from memory at the location of the program_counter and
        increase the program_counter by one (1).

        :return: Returns the byte read from memory.
        :rtype: int
        """
        data = self._read_byte(self.program_counter)
        self.program_counter += 1
        return data

    def _fetch_word(self) -> int:
        """
        Fetch a word from memory[program-counter].

        Fetch a word, two (2) bytes, from memory at the location of the
        program_counter and increase the program_counter by two (2).

        :return: int
        """
        data = self._read_word(self.program_counter)
        self.program_counter += 2
        return data

    def _read_byte(self, address: int) -> int:
        """
        Read a byte from memory[address].

        Read a byte from memory at the given address. As the bus is being
        accessed at the cost of one (1) cycle per byte read.

        :param address: The memory address to read from.
        :return: int
        """
        data = self.memory[address]
        self.cycles += 1
        return data

    def _read_word(self, address: int) -> int:
        """
        Read a word from memory[address].

        Read a word, two bytes, from memory starting at the given address. The
        read_byte() method is being used to read the memory after which the
        order of the low and high byte is applied.

        :param address: The memory address to read from.
        :return: int
        """
        if sys.byteorder == "little":
            data = self._read_byte(address) | (self._read_byte(address + 1) << 8)
        else:
            data = (self._read_byte(address) << 8) | self._read_byte(address + 1)
        return data

    def _write_byte(self, address: int, value: int) -> None:
        """
        Write a byte to memory[address].

        Write a byte to memory at the specified address. As the bus is being
        access at the cost of one (1) cycle per byte written. The Memory class
        will verify the memory address used and value being written to be both
        valid.

        :param int address: The memory address to write to.
        :param int value: The byte value to write.
        """
        self.memory[address] = value
        self.cycles += 1

    def _write_word(self, address: int, value: int) -> None:
        """
        Split a word to two bytes and write to memory.

        :param int address: The memory address to write to.
        :param int value: The word value (2 bytes) to write.
        """
        if sys.byteorder == "little":
            self._write_byte(address, value & 0xFF)
            self._write_byte(address + 1, (value >> 8) & 0xFF)
        else:
            self._write_byte(address, (value >> 8) & 0xFF)
            self._write_byte(address + 1, value & 0xFF)

    def _read_register_a(self) -> int:
        """
        Read the A register.

        :return: Value from Accumulator
        :rtype: int
        """
        self.cycles += 1
        return self.reg_a

    def _read_register_x(self) -> int:
        """
        Read the X register.

        :return: Value from X register
        :rtype: int
        """
        self.cycles += 1
        return self.reg_x

    def _read_register_y(self) -> int:
        """
        Read the Y register.

        :return: Value from Y register
        :rtype: int
        """
        self.cycles += 1
        return self.reg_y

    def push(self, data: int) -> None:
        """
        Push data, one (1) byte, to stack.

        :param int data: The byte to store on the stack
        :return: None
        """
        self.memory[self.stack_pointer] = data
        self.stack_pointer -= 1
        self.cycles += 1

    def pop(self) -> int:
        """
        Pop data, one (1) byte, from stack.

        :return: The byte read from the stack
        :rtype: int
        """
        self.stack_pointer += 1
        self.cycles += 1
        return self.memory[self.stack_pointer - 1]

    def _evaluate_flag_n(self, data: int) -> None:
        """
        Evaluate Negative Flag.

        :param int data: The data to evaluate
        :return: None
        """
        self.flag_n = (data & 0x80) != 0

    def _evaluate_flag_z(self, data: int) -> None:
        """
        Evaluate the Zero Flag.

        :param int data: The data to evaluate
        """
        if data == 0:
            self.flag_z = True
        else:
            self.flag_z = False

    def _evaluate_flags_nz(self, data: int) -> None:
        """
        Evaluate both the Negative and Zero Flag.

        :param int data: The data to evaluate
        """
        self._evaluate_flag_n(data)
        self._evaluate_flag_z(data)

    def execute(self, cycles: int = 0) -> None:
        """
        Execute code for X amount of cycles. Or until a breakpoint is reached.

        :param cycles: The number of cycles to execute
        :return: None
        """
        while (self.cycles < cycles) or (cycles == 0):
            opcode = self._fetch_byte()
            method_name = (
                "_ins_" + self._OPCODES[opcode] + "_" + self._ADDRESSING[opcode]
            )
            getattr(self, method_name)()

    def _ins_nop_imp(self) -> None:
        """
        NOP - No Operation.

        :return: None
        """
        self.cycles += 1

    def _ins_clc_imp(self) -> None:
        """
        CLC - Clear Carry Flag.

        :return: None
        """
        self.flag_c = False
        self.cycles += 1

    def _ins_cld_imp(self) -> None:
        """
        CLD - Clear Decimal Mode.

        :return: None
        """
        self.flag_d = False
        self.cycles += 1

    def _ins_cli_imp(self) -> None:
        """
        CLI - Clear Interrupt Disable.

        :return: None
        """
        self.flag_i = False
        self.cycles += 1

    def _ins_clv_imp(self) -> None:
        """
        CLV - Clear Overflow Flag.

        :return: None
        """
        self.flag_v = False
        self.cycles += 1

    def _ins_dec_zp(self) -> None:
        """
        DEC - Decrement Memory, Zero Page.

        :return: None
        """
        address = self._fetch_byte()
        self._write_byte(address, self._read_byte(address) - 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_dec_zpx(self) -> None:
        """
        DEC - Decrement Memory, Zero Page, X.

        :return: None
        """
        address = (self._fetch_byte() + self._read_register_x()) & 0xFF
        self._write_byte(address, self._read_byte(address) - 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_dec_abs(self) -> None:
        """
        DEC - Decrement Memory, Absolute.

        :return: None
        """
        address = self._fetch_word()
        self._write_byte(address, self._read_byte(address) - 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_dec_abx(self) -> None:
        """
        DEC - Decrement Memory, Absolute, X.

        :return: None
        """
        address = self._fetch_word() + self._read_register_x()
        self._write_byte(address, self._read_byte(address) - 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_dex_imp(self) -> None:
        """
        DEX - Decrement X Register.

        :return: None
        """
        self.reg_x = self._read_register_x() - 1
        self._evaluate_flags_nz(self.reg_x)

    def _ins_dey_imp(self) -> None:
        """
        DEY - Decrement Y Register.

        :return: None
        """
        self.reg_y = self._read_register_y() - 1
        self._evaluate_flags_nz(self.reg_y)

    def _ins_inc_zp(self) -> None:
        """
        INC - Increment Memory, Zero Page.

        :return: None
        """
        address = self._fetch_byte()
        self._write_byte(address, self._read_byte(address) + 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_inc_zpx(self) -> None:
        """
        INC - Increment Memory, Zero Page, X.

        :return: None
        """
        address = (self._fetch_byte() + self._read_register_x()) & 0xFF
        self._write_byte(address, self._read_byte(address) + 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_inc_abs(self) -> None:
        """
        INC - Increment Memory, Absolute.

        :return: None
        """
        address = self._fetch_word()
        self._write_byte(address, self._read_byte(address) + 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_inc_abx(self) -> None:
        """
        INC - Increment Memory, Absolute, X.

        :return: None
        """
        address = self._fetch_word() + self._read_register_x()
        self._write_byte(address, self._read_byte(address) + 1)
        self._evaluate_flags_nz(self.memory[address])
        self.cycles += 1

    def _ins_inx_imp(self) -> None:
        """
        INX - Increment X Register.

        :return: None
        """
        self.reg_x = self._read_register_x() + 1
        self._evaluate_flags_nz(self.reg_x)

    def _ins_iny_imp(self) -> None:
        """
        INY - Increment Y Register.

        :return: None
        """
        self.reg_y = self._read_register_y() + 1
        self._evaluate_flags_nz(self.reg_y)

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

    def _ins_lda_zp(self) -> None:
        """
        LDA (0xA5) - Load Accumulator, Zero Page.

        Load the value stored at the memory location that is after the opcode
        directly into accumulator and then evaluate accumulator for flags Zero
        and Negative. The memory location is a single byte and within the Zero
        Page memory range of 0-255.

        Assembly example:

        ```
        LDA nn
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 2 bytes and 3 cycles to complete.
        """
        self.reg_a = self._read_byte(self._fetch_byte() & 0xFF)
        self._evaluate_flags_nz(self.reg_a)

    def _ins_lda_zpx(self) -> None:
        """
        LDA (0xB5) - Load Accumulator, Zero Page, X.

        Load the value stored at the memory location that is stored after the
        opcode and increased with the value in register X before copied
        directly into accumulator and then evaluate accumulator for flags Zero
        and Negative. The memory location is a single byte and within the Zero
        Page memory range of 0-255.

        Assembly example:

        ```
        LDX #nn
        LDA nn,X
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 2 bytes and 5 cycles to complete.
        """
        self.cycles += 1  # TODO: Why is the extra cycle required?
        self.reg_a = self._read_byte(
            (self._fetch_byte() + self._read_register_x()) & 0xFF
        )
        self._evaluate_flags_nz(self.reg_a)

    def _ins_lda_abs(self) -> None:
        """
        LDA (0xAD) - Load Accumulator, Absolute.

        Load the value stored at the memory location that is stored after the
        opcode before copied directly into accumulator and then evaluate
        accumulator for flags Zero and Negative. The memory location are two
        bytes and can address any memory location.

        Assembly example:

        ```
        LDA nnnn
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 3 bytes and 4 cycles to complete.
        """
        self.reg_a = self._read_byte(self._fetch_word())
        self._evaluate_flags_nz(self.reg_a)

    def _ins_lda_abx(self) -> None:
        """
        LDA (0xBD) - Load Accumulator, Absolute, X.

        Load the value stored at the memory location that is stored after the
        opcode and increased with the value in register X before copied
        directly into accumulator and then evaluate accumulator for flags Zero
        and Negative. The memory location are two bytes and can address any
        memory location.

        Assembly example:

        ```
        LDA nnnn,X
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 3 bytes and 4 (+1 if page crossed) cycles to complete.
        """
        address = self._fetch_word()
        self.reg_a = self._read_byte(address + self.reg_x)
        self._evaluate_flags_nz(self.reg_a)
        # Simulate page crossing
        if ((address & 0xFF) + self.reg_x) >= 0xFF:
            self.cycles += 1

    def _ins_lda_aby(self) -> None:
        """
        LDA (0xB9) - Load Accumulator, Absolute, Y.

        Load the value stored at the memory location that is stored after the
        opcode and increased with the value in register Y before copied
        directly into accumulator and then evaluate accumulator for flags Zero
        and Negative. The memory location are two bytes and can address any
        memory location.

        Assembly example:
        ```
        LDA nnnn,Y
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 3 bytes and 4 (+1 if page crossed) cycles to complete.
        """
        address = self._fetch_word()
        self.reg_a = self._read_byte(address + self.reg_y)
        self._evaluate_flags_nz(self.reg_a)
        # Simulate page crossing
        if ((address & 0xFF) + self.reg_y) >= 0xFF:
            self.cycles += 1

    def _ins_lda_inx(self) -> None:
        """
        LDA (0xA1) - Load Accumulator, Indexed Indirect.

        Load the value stored at the memory location that is stored after the
        opcode and increased with the value in register X before copied
        directly into accumulator and then evaluate accumulator for flags Zero
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
        LDY #nn
        LDA (nn,X)
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 2 bytes and 6 cycles to complete.
        """
        self.reg_a = self._read_byte(
            self._read_word(((self._fetch_byte() + self.reg_x) & 0xFF))
        )
        self._evaluate_flags_nz(self.reg_a)
        self.cycles += 1  # TODO: Why is the extra cycle required?

    def _ins_lda_iny(self) -> None:
        """
        LDA (0xB1) - Load Accumulator, Indirect Indexed.

        Assembly example:

        ```
        LDY #nn
        LDA (nn),Y
        ```

        Affected flags:
        - Zero Flag: Set if A = 0
        - Negative Flag: Set if bit 7 of A is set

        The instruction costs 2 bytes and 5 (+1 if page crossed) cycles to complete.
        """
        address = self._read_word(self._fetch_byte())
        self.reg_a = self._read_byte(address + self.reg_y)
        self._evaluate_flags_nz(self.reg_a)
        # Simulate page crossing
        if ((address & 0xFF) + self.reg_y) >= 0xFF:
            self.cycles += 1

    def _ins_ldx_imm(self) -> None:
        """
        LDX (0xA2) - Load X Register, Immediate.

        Load the value stored after the opcode directly into register X
        and then evaluate register X for flags Zero and Negative.

        Assembly example:

        ```
        LDX #$04
        ```

        The instruction costs 2 bytes and 2 cycles to complete.
        """
        self.reg_x = self._fetch_byte()
        self._evaluate_flags_nz(self.reg_x)

    def _ins_ldx_zp(self) -> None:
        """
        LDX (0xA6) - Load X Register, Zero Page.

        :return: None
        """
        self.reg_x = self._read_byte(self._fetch_byte())
        self._evaluate_flags_nz(self.reg_x)

    def _ins_ldx_zpy(self) -> None:
        """
        LDX (0xB6) - Load X Register, Zero Page, Y.

        The instruction costs 2 bytes and 5 cycles to complete.
        """
        self.reg_x = self._read_byte(
            (self._fetch_byte() + self._read_register_y()) & 0xFF
        )
        self._evaluate_flags_nz(self.reg_x)
        self.cycles += 1  # TODO: Why is the extra cycle required?

    def _ins_ldx_abs(self) -> None:
        """
        LDX - Load X Register, Absolute.

        :return: None
        """
        self.reg_x = self._read_byte(self._fetch_word())
        self._evaluate_flags_nz(self.reg_x)

    def _ins_ldx_aby(self) -> None:
        """
        LDX - Load X Register, Absolute, Y.

        The instruction costs 3 bytes and 4 (+1 if page crossed) cycles to complete.
        """
        address = self._fetch_word()
        self.reg_x = self._read_byte(address + self.reg_y)
        self._evaluate_flags_nz(self.reg_x)
        # Simulate page crossing
        if ((address & 0xFF) + self.reg_y) >= 0xFF:
            self.cycles += 1

    def _ins_ldy_imm(self) -> None:
        """
        LDY (0x40) - Load Y Register, Immediate.

        Load the value stored after the opcode directly into register Y
        and then evaluate register Y for flags Zero and Negative.

        Assembly example:
        ```
        LDY #$04
        ```

        Affected flags:
        - Zero Flag: Set if Y = 0
        - Negative Flag: Set if bit 7 of Y is set

        The instruction costs 2 bytes and 2 cycles to complete.
        """
        self.reg_y = self._fetch_byte()
        self._evaluate_flags_nz(self.reg_y)

    def _ins_ldy_zp(self) -> None:
        """
        LDY (0xA4) - Load Y Register, Zero Page.

        Load the value stored at the memory location that is after the opcode
        directly into register Y and then evaluate register Y for flags Zero
        and Negative. The memory location is a single byte and within the Zero
        Page memory range of 0-255.
        Assembly example:

        Assembly example:
        ```
        LDY nn
        ```

        Affected flags:
        - Zero Flag: Set if Y = 0
        - Negative Flag: Set if bit 7 of Y is set

        The instruction costs 2 bytes and 3 cycles to complete.
        """
        self.reg_y = self._read_byte(self._fetch_byte())
        self._evaluate_flags_nz(self.reg_y)

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

    def _ins_ldy_abs(self) -> None:
        """
        LDA (0xAC) - Load Y Register, Absolute.

        Load the value stored at the memory location that is stored after the
        opcode before copied directly into register Y and then evaluate
        register Y for flags Zero and Negative. The memory location are two
        bytes and can address any memory location.

        Assembly example:

        ```
        LDY nnnn
        ```

        Affected flags:
        - Zero Flag: Set if Y = 0
        - Negative Flag: Set if bit 7 of Y is set

        The instruction costs 3 bytes and 4 cycles to complete.
        """
        self.reg_y = self._read_byte(self._fetch_word())
        self._evaluate_flags_nz(self.reg_y)

    def _ins_ldy_abx(self) -> None:
        """
        LDA (0xBC) - Load Y Register, Absolute, X.

        Load the value stored at the memory location that is stored after the
        opcode and increased with the value in register X before copied
        directly into register Y and then evaluate register Y for flags Zero
        and Negative. The memory location are two bytes and can address any
        memory location.

        Assembly example:

        ```
        LDY nnnn,X
        ```

        Affected flags:
        - Zero Flag: Set if Y = 0
        - Negative Flag: Set if bit 7 of Y is set

        The instruction costs 3 bytes and 4 (+1 if page crossed) cycles to complete.
        """
        address = self._fetch_word()
        self.reg_y = self._read_byte(address + self.reg_x)
        self._evaluate_flags_nz(self.reg_y)
        # Simulate page crossing
        if ((address & 0xFF) + self.reg_x) >= 0xFF:
            self.cycles += 1

    def _ins_sec_imp(self) -> None:
        """
        SEC - Set Carry Flag.

        :return: None
        """
        self.flag_c = True
        self.cycles += 1

    def _ins_sed_imp(self) -> None:
        """
        SED - Set Decimal Mode.

        :return: None
        """
        self.flag_d = True
        self.cycles += 1

    def _ins_sei_imp(self) -> None:
        """
        SEI - Set Interrupt Disable.

        :return: None
        """
        self.flag_i = True
        self.cycles += 1

    def _ins_sta_zp(self) -> None:
        """
        STA (0x85) - Store Accumulator, Zero Page.

        Store the value in the accumulator at the memory location that is
        stored after the opcode. The memory location is a single byte and
        within the Zero Page memory range of 0-255. The value in the
        accumulator is written to the memory location without any modification.

        Assembly example:
        ```
        STA nn
        ```

        Affected flags:
        - None

        The instruction costs 2 bytes and 3 cycles to complete.
        """
        self._write_byte(self._fetch_byte(), self.reg_a)

    def _ins_sta_zpx(self) -> None:
        """
        STA (0x95) - Store Accumulator, Zero Page, X.

        :return: None
        """
        self._write_byte((self._fetch_byte() + self.reg_x) & 0xFF, self.reg_a)

    def _ins_sta_abs(self) -> None:
        """
        STA (0x8D) - Store Accumulator, Absolute.

        :return: None
        """
        self._write_byte(self._fetch_word(), self.reg_a)

    def _ins_sta_abx(self) -> None:
        """
        STA (0x9D) - Store Accumulator, Absolute, X.

        :return: None
        """
        self._write_byte(self._fetch_word() + self._read_register_x(), self.reg_a)

    def _ins_sta_aby(self) -> None:
        """
        STA (0x99) - Store Accumulator, Absolute, Y.

        :return: None
        """
        self._write_byte(self._fetch_word() + self._read_register_y(), self.reg_a)

    def _ins_sta_inx(self) -> None:
        """
        STA (0x81) - Store Accumulator, Indexed Indirect.

        :return: None
        """
        self._write_byte(
            self._read_byte(
                self._read_word(((self._fetch_byte() + self.reg_x) & 0xFF))
            ),
            self.reg_a,
        )

    def _ins_sta_iny(self) -> None:
        """
        STA (0x91) - Store Accumulator, Indirect Indexed.

        :return: None
        """
        self._write_byte(
            self._read_byte(self._read_word(self._fetch_byte()) + self.reg_y),
            self.reg_a,
        )

    def _ins_stx_zp(self) -> None:
        """
        STA - Store X Register, Zero Page.

        :return: None
        """
        self._write_byte(self._fetch_byte(), self.reg_x)

    def _ins_stx_zpy(self) -> None:
        """
        STA - Store Y Register, Zero Page, X.

        :return: None
        """
        self._write_byte(
            (self._fetch_byte() + self._read_register_y()) & 0xFF, self.reg_x
        )

    def _ins_stx_abs(self) -> None:
        """
        STA - Store X Register, Absolute.

        :return: None
        """
        self._write_byte(self._fetch_word(), self.reg_x)

    def _ins_sty_zp(self) -> None:
        """
        STA - Store Y Register, Zero Page.

        :return: None
        """
        self._write_byte(self._fetch_byte(), self.reg_y)

    def _ins_sty_zpx(self) -> None:
        """
        STA - Store Y Register, Zero Page, X.

        :return: None
        """
        self._write_byte(
            (self._fetch_byte() + self._read_register_x()) & 0xFF, self.reg_y
        )

    def _ins_sty_abs(self) -> None:
        """
        STA - Store Y Register, Absolute.

        :return: None
        """
        self._write_byte(self._fetch_word(), self.reg_y)

    def _ins_tax_imp(self) -> None:
        """
        TAX - Transfer Accumulator to X.

        :return: None
        """
        self.reg_x = self._read_register_a()
        self._evaluate_flags_nz(self.reg_x)

    def _ins_tay_imp(self) -> None:
        """
        TAY - Transfer Accumulator to Y.

        :return: None
        """
        self.reg_y = self._read_register_a()
        self._evaluate_flags_nz(self.reg_y)

    def _ins_tsx_imp(self) -> None:
        """
        TSX - Transfer Stack Pointer to X.

        :return: None
        """
        self.reg_x = self.pop()
        self._evaluate_flags_nz(self.reg_x)

    def _ins_txa_imp(self) -> None:
        """
        TXA - Transfer Register X to Accumulator.

        :return: None
        """
        self.reg_a = self._read_register_x()
        self._evaluate_flags_nz(self.reg_a)

    def _ins_txs_imp(self) -> None:
        """
        TXS - Transfer Register X to Stack Pointer.

        :return: None
        """
        self.push(self.reg_x)

    def _ins_tya_imp(self) -> None:
        """
        TYA - Transfer Register Y to Accumulator.

        :return: None
        """
        self.reg_a = self._read_register_y()
        self._evaluate_flags_nz(self.reg_a)

    def _ins_pha_imp(self) -> None:
        """
        PHA - Push Accumulator.

        TODO: Add check to not cross page

        :return: None
        """
        self.memory[self.stack_pointer] = self._read_register_a()
        self.stack_pointer -= 1
        self.cycles += 1

    def _ins_pla_imp(self) -> None:
        """
        PLA - Pull Accumulator.

        TODO: Add check to not cross page

        :return: None
        """
        self.reg_a = self.memory[self.stack_pointer]
        self.stack_pointer += 1
        self.cycles += 1
        self._evaluate_flags_nz(self.reg_a)

    def _ins_php_imp(self) -> None:
        """
        Push Processor Status, Implied.

        return: None
        """
        flags = 0x00
        if self.flag_n:
            flags = flags | (1 << 1)
        if self.flag_v:
            flags = flags | (1 << 2)
        if self.flag_b:
            flags = flags | (1 << 3)
        if self.flag_d:
            flags = flags | (1 << 4)
        if self.flag_i:
            flags = flags | (1 << 5)
        if self.flag_z:
            flags = flags | (1 << 6)
        if self.flag_c:
            flags = flags | (1 << 7)
        self.push(flags)
        self.cycles += 1

    def _ins_plp_imp(self) -> None:
        """
        Pull Processor Status.

        TODO: Implement instruction and test
        TODO: Add check to not cross page

        :return: None
        """
        flags = self.pop()
        # print(flags)
        if not flags & (1 << 1):
            self.flag_n = False
        if not flags & (1 << 2):
            self.flag_v = False
        if not flags & (1 << 3):
            self.flag_b = False
        if not flags & (1 << 4):
            self.flag_d = False
        if not flags & (1 << 5):
            self.flag_i = False
        if not flags & (1 << 6):
            self.flag_z = False
        if not flags & (1 << 7):
            self.flag_c = False
        self.cycles += 2
