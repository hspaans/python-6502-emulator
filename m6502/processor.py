"""
Emulation of the MOT-6502 Processor
"""

import m6502


class Processor:
    """
    MOT-6502 Processor
    """

    def __init__(self, memory: m6502.memory) -> None:
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
        """Reset processor to initial state and reset memory"""
        self.program_counter = 0xFFFC
        self.stack_pointer = 0x0100
        self.flag_d = False
        for address in range(self.memory.size):
            self.memory[address] = 0
