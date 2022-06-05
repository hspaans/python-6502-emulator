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

    def __init__(self, memory: m6502.memory) -> None:
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

    def reset(self) -> None:
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

    def fetch_byte(self) -> int:
        """
        Fetch a byte from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.read_byte(self.program_counter)
        self.program_counter += 1
        return data

    def fetch_word(self) -> int:
        """
        Fetch a word from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.read_word(self.program_counter)
        self.program_counter += 2
        return data

    def read_byte(self, address: int) -> int:
        """
        Read a byte from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.memory[address]
        self.cycles += 1
        return data

    def read_word(self, address: int) -> int:
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

    def write_byte(self, address: int, value: int) -> None:
        """
        Write a byte to memory.

        :param address: The address to write to
        :param value: The value to write
        :return: None
        """
        self.memory[address] = value
        self.cycles += 1

    def write_word(self, address: int, value: int) -> None:
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

    def execute(self, cycles: int = 0) -> None:
        """
        Execute code for X amount of cycles. Or until a breakpoint is reached.

        :param cycles: The number of cycles to execute
        :return: None
        """
        while (self.cycles < cycles) or (cycles == 0):
            opcode = self.fetch_byte()
            eval("self.ins_" + self.OPCODES[opcode] + "_" + self.ADDRESSING[opcode] + "()")  # noqa: PLW0123

    def ins_nop_imp(self) -> None:
        """
        NOP - No Operation.

        :return: None
        """
        self.cycles += 1

    def ins_clc_imp(self) -> None:
        """
        CLC - Clear Carry Flag.

        :return: None
        """
        self.flag_c = False
        self.cycles += 1

    def ins_cld_imp(self) -> None:
        """
        CLD - Clear Decimal Mode.

        :return: None
        """
        self.flag_d = False
        self.cycles += 1

    def ins_cli_imp(self) -> None:
        """
        CLI - Clear Interrupt Disable.

        :return: None
        """
        self.flag_i = False
        self.cycles += 1

    def ins_clv_imp(self) -> None:
        """
        CLV - Clear Overflow Flag.

        :return: None
        """
        self.flag_v = False
        self.cycles += 1

    def ins_sec_imp(self) -> None:
        """
        SEC - Set Carry Flag.

        :return: None
        """
        self.flag_c = True
        self.cycles += 1

    def ins_sed_imp(self) -> None:
        """
        SED - Set Decimal Mode.

        :return: None
        """
        self.flag_d = True
        self.cycles += 1

    def ins_sei_imp(self) -> None:
        """
        SEI - Set Interrupt Disable.

        :return: None
        """
        self.flag_i = True
        self.cycles += 1

    def ins_dex_imp(self) -> None:
        """
        DEC - Decrement X Register.

        :return: None
        """
        self.reg_x -= 1
        self.cycles += 1
        if self.reg_x == 0:
            self.flag_z = True
        else:
            self.flag_z = False
        if self.reg_x & 0x80:
            self.flag_n = True
        else:
            self.flag_n = False

    def ins_dey_imp(self) -> None:
        """
        DEC - Decrement X Register.

        :return: None
        """
        self.reg_y -= 1
        self.cycles += 1
        if self.reg_y == 0:
            self.flag_z = True
        else:
            self.flag_z = False
        if self.reg_y & 0x80:
            self.flag_n = True
        else:
            self.flag_n = False

    def ins_inx_imp(self) -> None:
        """
        INX - Increment X Register.

        :return: None
        """
        self.reg_x += 1
        self.cycles += 1
        if self.reg_x == 0:
            self.flag_z = True
        else:
            self.flag_z = False
        if self.reg_x & 0x80:
            self.flag_n = True
        else:
            self.flag_n = False

    def ins_iny_imp(self) -> None:
        """
        INY - Increment Y Register.

        :return: None
        """
        self.reg_y += 1
        self.cycles += 1
        if self.reg_y == 0:
            self.flag_z = True
        else:
            self.flag_z = False
        if self.reg_y & 0x80:
            self.flag_n = True
        else:
            self.flag_n = False
