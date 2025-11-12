"""Emulation of the MOT-6502 Processor."""
import sys

import m6502


class Processor:
    """MOT-6502 Processor."""

    ADDRESSING = [
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

    OPCODES = [
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

    def __init__(self: object, memory: m6502.memory) -> None:
        """
        Initialize the processor.

        :param memory: The memory to use
        :return: None
        """
        self.memory = memory
        self.reg_a = 0  # Accumlator A
        self.reg_y = 0  # Incex Register Y
        self.reg_x = 0  # Incex Register X

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

    def reset(self: object) -> None:
        """
        Reset processor to initial state.

        :return: None
        """
        self.program_counter = 0xFCE2  # Hardcoded start vector post-reset
        self.stack_pointer   = 0x01FD  # Hardcoded stack pointer post-reset
        self.cycles          = 0

        self.flag_i = True
        self.flag_d = False
        self.flag_b = True

    def fetch_byte(self: object) -> int:
        """
        Fetch a byte from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.read_byte(self.program_counter)
        self.program_counter += 1
        return data

    def fetch_word(self: object) -> int:
        """
        Fetch a word from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.read_word(self.program_counter)
        self.program_counter += 2
        return data

    def read_byte(self: object, address: int) -> int:
        """
        Read a byte from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.memory[address]
        self.cycles += 1
        return data

    def read_word(self: object, address: int) -> int:
        """
        Read a word from memory.

        :param address: The address to read from
        :return: int
        """
        if sys.byteorder == "little":
            data = self.read_byte(address) | (self.read_byte(address + 1) << 8)
        else:
            data = (self.read_byte(address) << 8) | self.read_byte(address + 1)
        return data

    def write_byte(self: object, address: int, value: int) -> None:
        """
        Write a byte to memory.

        :param address: The address to write to
        :param value: The value to write
        :return: None
        """
        self.memory[address] = value
        self.cycles += 1

    def write_word(self: object, address: int, value: int) -> None:
        """
        Split a word to two bytes and write to memory.

        :param address: The address to write to
        :param value: The value to write
        :return: None
        """
        if sys.byteorder == "little":
            self.write_byte(address, value & 0xFF)
            self.write_byte(address + 1, (value >> 8) & 0xFF)
        else:
            self.write_byte(address, (value >> 8) & 0xFF)
            self.write_byte(address + 1, value & 0xFF)

    def read_register_a(self: object) -> int:
        """
        Read the A register.

        :return: int
        """
        self.cycles += 1
        return self.reg_a

    def read_register_x(self: object) -> int:
        """
        Read the X register.

        :return: int
        """
        self.cycles += 1
        return self.reg_x

    def read_register_y(self: object) -> int:
        """
        Read the Y register.

        :return: int
        """
        self.cycles += 1
        return self.reg_y

    def push(self: object, data: int) -> None:
        """
        Push data to stack.

        :return: None
        """
        self.memory[self.stack_pointer] = data
        self.stack_pointer -= 1
        self.cycles += 1

    def pop(self: object) -> int:
        """
        Pop data from stack.

        :return: int
        """
        self.stack_pointer += 1
        self.cycles += 1
        return self.memory[self.stack_pointer - 1]

    def evaluate_flag_n(self: object, data: int) -> None:
        """
        Evaluate negative flag.

        :param data: The data to evaluate
        :return: None
        """
        self.flag_n = (data & 0x80) != 0

    def evaluate_flag_z(self: object, data: int) -> None:
        """
        Evaluate the Zero Flag.

        :param data: The data to evaluate
        :return: None
        """
        if data == 0:
            self.flag_z = True
        else:
            self.flag_z = False

    def execute(self: object, cycles: int = 0) -> None:
        """
        Execute code for X amount of cycles. Or until a breakpoint is reached.

        :param cycles: The number of cycles to execute
        :return: None
        """
        while (self.cycles < cycles) or (cycles == 0):
            opcode = self.fetch_byte()
            name = f"ins_{self.OPCODES[opcode]}_{self.ADDRESSING[opcode]}"
            method = getattr(self, name)
            method()

    def ins_nop_imp(self: object) -> None:
        """
        NOP - No Operation.

        :return: None
        """
        self.cycles += 1

    def ins_clc_imp(self: object) -> None:
        """
        CLC - Clear Carry Flag.

        :return: None
        """
        self.flag_c = False
        self.cycles += 1

    def ins_cld_imp(self: object) -> None:
        """
        CLD - Clear Decimal Mode.

        :return: None
        """
        self.flag_d = False
        self.cycles += 1

    def ins_cli_imp(self: object) -> None:
        """
        CLI - Clear Interrupt Disable.

        :return: None
        """
        self.flag_i = False
        self.cycles += 1

    def ins_clv_imp(self: object) -> None:
        """
        CLV - Clear Overflow Flag.

        :return: None
        """
        self.flag_v = False
        self.cycles += 1

    def ins_dec_zp(self: object) -> None:
        """
        DEC - Decrement Memory, Zero Page.

        :return: None
        """
        address = self.fetch_byte()
        self.write_byte(address, self.read_byte(address) - 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_dec_zpx(self: object) -> None:
        """
        DEC - Decrement Memory, Zero Page, X.

        :return: None
        """
        address = (self.fetch_byte() + self.read_register_x()) & 0xFF
        self.write_byte(address, self.read_byte(address) - 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_dec_abs(self: object) -> None:
        """
        DEC - Decrement Memory, Absolute.

        :return: None
        """
        address = self.fetch_word()
        self.write_byte(address, self.read_byte(address) - 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_dec_abx(self: object) -> None:
        """
        DEC - Decrement Memory, Absolute, X.

        :return: None
        """
        address = self.fetch_word() + self.read_register_x()
        self.write_byte(address, self.read_byte(address) - 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_dex_imp(self: object) -> None:
        """
        DEX - Decrement X Register.

        :return: None
        """
        self.reg_x = self.read_register_x() - 1
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_dey_imp(self: object) -> None:
        """
        DEY - Decrement Y Register.

        :return: None
        """
        self.reg_y = self.read_register_y() - 1
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_inc_zp(self: object) -> None:
        """
        INC - Increment Memory, Zero Page.

        :return: None
        """
        address = self.fetch_byte()
        self.write_byte(address, self.read_byte(address) + 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_inc_zpx(self: object) -> None:
        """
        INC - Increment Memory, Zero Page, X.

        :return: None
        """
        address = (self.fetch_byte() + self.read_register_x()) & 0xFF
        self.write_byte(address, self.read_byte(address) + 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_inc_abs(self: object) -> None:
        """
        INC - Increment Memory, Absolute.

        :return: None
        """
        address = self.fetch_word()
        self.write_byte(address, self.read_byte(address) + 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_inc_abx(self: object) -> None:
        """
        INC - Increment Memory, Absolute, X.

        :return: None
        """
        address = self.fetch_word() + self.read_register_x()
        self.write_byte(address, self.read_byte(address) + 1)
        self.evaluate_flag_n(self.memory[address])
        self.evaluate_flag_z(self.memory[address])
        self.cycles += 1

    def ins_inx_imp(self: object) -> None:
        """
        INX - Increment X Register.

        :return: None
        """
        self.reg_x = self.read_register_x() + 1
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_iny_imp(self: object) -> None:
        """
        INY - Increment Y Register.

        :return: None
        """
        self.reg_y = self.read_register_y() + 1
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_lda_imm(self: object) -> None:
        """
        LDA - Load Accumulator, Immediate.

        :return: None
        """
        self.reg_a = self.fetch_byte()
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_lda_zp(self: object) -> None:
        """
        LDA - Load Accumulator, Zero Page.

        :return: None
        """
        self.reg_a = self.read_byte(
            self.fetch_byte()
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_lda_zpx(self: object) -> None:
        """
        LDA - Load Accumulator, Zero Page, X.

        :return: None
        """
        self.reg_a = self.read_byte(
            (self.fetch_byte() + self.read_register_x()) & 0xFF
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_lda_abs(self: object) -> None:
        """
        LDA - Load Accumulator, Absolute.

        :return: None
        """
        self.reg_a = self.read_byte(
            self.fetch_word()
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_lda_abx(self: object) -> None:
        """
        LDA - Load Accumulator, Absolute, X.

        TODO: Using register X directly otherwise we use too many cycles.

        :return: None
        """
        self.reg_a = self.read_byte(
            self.fetch_word() + self.reg_x
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_lda_aby(self: object) -> None:
        """
        LDA - Load Accumulator, Absolute, Y.

        TODO: Using register Y directly otherwise we use too many cycles.

        :return: None
        """
        self.reg_a = self.read_byte(
            self.fetch_word() + self.reg_y
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_lda_inx(self: object) -> None:
        """
        LDA - Load Accumulator, Indexed Indirect.

        :return: None
        """
        self.reg_a = self.read_byte(
            self.read_word(
                ((self.fetch_byte() + self.reg_x) & 0xFF)
            )
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)
        self.cycles += 1

    def ins_lda_iny(self: object) -> None:
        """
        LDA - Load Accumulator, Indirect Indexed.

        :return: None
        """
        self.reg_a = self.read_byte(
            self.read_word(
                self.fetch_byte()
            ) + self.reg_y
        )
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_ldx_imm(self: object) -> None:
        """
        LDA - Load X Register, Immediate.

        :return: None
        """
        self.reg_x = self.fetch_byte()
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_ldx_zp(self: object) -> None:
        """
        LDA - Load X Register, Zero Page.

        :return: None
        """
        self.reg_x = self.read_byte(self.fetch_byte())
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_ldx_zpy(self: object) -> None:
        """
        LDA - Load X Register, Zero Page, Y.

        :return: None
        """
        self.reg_x = self.read_byte(
            (self.fetch_byte() + self.read_register_y()) & 0xFF
        )
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_ldx_abs(self: object) -> None:
        """
        LDA - Load X Register, Absolute.

        :return: None
        """
        self.reg_x = self.read_byte(
            self.fetch_word()
        )
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_ldx_aby(self: object) -> None:
        """
        LDA - Load X Register, Absolute, Y.

        TODO: Using register Y directly otherwise we use too many cycles.

        :return: None
        """
        self.reg_x = self.read_byte(
            self.fetch_word() + self.reg_y
        )
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_ldy_imm(self: object) -> None:
        """
        LDA - Load Y Register, Immediate.

        :return: None
        """
        self.reg_y = self.fetch_byte()
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_ldy_zp(self: object) -> None:
        """
        LDA - Load Y Register, Zero Page.

        :return: None
        """
        self.reg_y = self.read_byte(
            self.fetch_byte()
        )
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_ldy_zpx(self: object) -> None:
        """
        LDA - Load Y Register, Zero Page, X.

        :return: None
        """
        self.reg_y = self.read_byte(
            (self.fetch_byte() + self.read_register_x()) & 0xFF
        )
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_ldy_abs(self: object) -> None:
        """
        LDA - Load Y Register, Absolute.

        :return: None
        """
        self.reg_y = self.read_byte(
            self.fetch_word()
        )
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_ldy_abx(self: object) -> None:
        """
        LDA - Load Y Register, Absolute, X.

        TODO: Using register X directly otherwise we use too many cycles.

        :return: None
        """
        self.reg_y = self.read_byte(
            self.fetch_word() + self.reg_x
        )
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_sec_imp(self: object) -> None:
        """
        SEC - Set Carry Flag.

        :return: None
        """
        self.flag_c = True
        self.cycles += 1

    def ins_sed_imp(self: object) -> None:
        """
        SED - Set Decimal Mode.

        :return: None
        """
        self.flag_d = True
        self.cycles += 1

    def ins_sei_imp(self: object) -> None:
        """
        SEI - Set Interrupt Disable.

        :return: None
        """
        self.flag_i = True
        self.cycles += 1

    def ins_sta_zp(self: object) -> None:
        """
        STA - Store Accumulator, Zero Page.

        :return: None
        """
        self.write_byte(
            self.fetch_byte(),
            self.reg_a
        )

    def ins_sta_zpx(self: object) -> None:
        """
        STA - Store Accumulator, Zero Page, X.

        :return: None
        """
        self.write_byte(
            (self.fetch_byte() + self.read_register_x()) & 0xFF,
            self.reg_a
        )

    def ins_sta_abs(self: object) -> None:
        """
        STA - Store Accumulator, Absolute.

        :return: None
        """
        self.write_byte(
            self.fetch_word(),
            self.reg_a
        )

    def ins_sta_abx(self: object) -> None:
        """
        STA - Store Accumulator, Absolute, X.

        TODO: Using register X directly otherwise we use too many cycles.

        :return: None
        """
        self.write_byte(
            self.read_byte(
                self.fetch_word() + self.reg_x
            ),
            self.reg_a
        )

    def ins_sta_aby(self: object) -> None:
        """
        STA - Store Accumulator, Absolute, Y.

        TODO: Using register Y directly otherwise we use too many cycles.

        :return: None
        """
        self.write_byte(
            self.read_byte(
                self.fetch_word() + self.reg_y
            ),
            self.reg_a
        )

    def ins_sta_inx(self: object) -> None:
        """
        STA - Store Accumulator, Indexed Indirect.

        :return: None
        """
        self.write_byte(
            self.read_byte(
                self.read_word(
                    ((self.fetch_byte() + self.reg_x) & 0xFF)
                )
            ),
            self.reg_a
        )

    def ins_sta_iny(self: object) -> None:
        """
        LDA - Store Accumulator, Indirect Indexed.

        :return: None
        """
        self.write_byte(
            self.read_byte(
                self.read_word(
                    self.fetch_byte()
                ) + self.reg_y
            ),
            self.reg_a
        )

    def ins_stx_zp(self: object) -> None:
        """
        STA - Store X Register, Zero Page.

        :return: None
        """
        self.write_byte(
            self.fetch_byte(),
            self.reg_x
        )

    def ins_stx_zpy(self: object) -> None:
        """
        STA - Store Y Register, Zero Page, X.

        :return: None
        """
        self.write_byte(
            (self.fetch_byte() + self.read_register_y()) & 0xFF,
            self.reg_x
        )

    def ins_stx_abs(self: object) -> None:
        """
        STA - Store X Register, Absolute.

        :return: None
        """
        self.write_byte(
            self.fetch_word(),
            self.reg_x
        )

    def ins_sty_zp(self: object) -> None:
        """
        STA - Store Y Register, Zero Page.

        :return: None
        """
        self.write_byte(
            self.fetch_byte(),
            self.reg_y
        )

    def ins_sty_zpx(self: object) -> None:
        """
        STA - Store Y Register, Zero Page, X.

        :return: None
        """
        self.write_byte(
            (self.fetch_byte() + self.read_register_x()) & 0xFF,
            self.reg_y
        )

    def ins_sty_abs(self: object) -> None:
        """
        STA - Store Y Register, Absolute.

        :return: None
        """
        self.write_byte(
            self.fetch_word(),
            self.reg_y
        )

    def ins_tax_imp(self: object) -> None:
        """
        TAX - Transfer Accumulator to X.

        :return: None
        """
        self.reg_x = self.read_register_a()
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_tay_imp(self: object) -> None:
        """
        TAY - Transfer Accumulator to Y.

        :return: None
        """
        self.reg_y = self.read_register_a()
        self.evaluate_flag_z(self.reg_y)
        self.evaluate_flag_n(self.reg_y)

    def ins_tsx_imp(self: object) -> None:
        """
        TSX - Transfer Stack Pointer to X.

        :return: None
        """
        self.reg_x = self.pop()
        self.evaluate_flag_z(self.reg_x)
        self.evaluate_flag_n(self.reg_x)

    def ins_txa_imp(self: object) -> None:
        """
        TXA - Transfer Register X to Accumulator.

        :return: None
        """
        self.reg_a = self.read_register_x()
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_txs_imp(self: object) -> None:
        """
        TXS - Transfer Register X to Stack Pointer.

        :return: None
        """
        self.push(self.reg_x)

    def ins_tya_imp(self: object) -> None:
        """
        TYA - Transfer Register Y to Accumulator.

        :return: None
        """
        self.reg_a = self.read_register_y()
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_pha_imp(self: object) -> None:
        """
        PHA - Push Accumulator.

        TODO: Add check to not cross page

        :return: None
        """
        self.memory[self.stack_pointer] = self.read_register_a()
        self.stack_pointer -= 1
        self.cycles += 1

    def ins_pla_imp(self: object) -> None:
        """
        PLA - Pull Accumulator.

        TODO: Add check to not cross page

        :return: None
        """
        self.reg_a = self.memory[self.stack_pointer]
        self.stack_pointer += 1
        self.cycles += 1
        self.evaluate_flag_z(self.reg_a)
        self.evaluate_flag_n(self.reg_a)

    def ins_php_imp(self: object) -> None:
        """
        Push Processor Statys, Implied.

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

    def ins_plp_imp(self: object) -> None:
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
