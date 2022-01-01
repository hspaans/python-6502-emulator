"""
Emulation of the MOT-6502 memory
"""


class Memory:
    """
    Memory bank for MOT-6502 systems
    """

    def __init__(self, size: int = 65536) -> None:
        self.size = size
        self.memory = [0] * self.size
        for i in range(self.size):
            self.memory[i] = 0x00

    def __getitem__(self, address: int) -> int:
        return self.memory[address]

    def __setitem__(self, address: int, value: int) -> int:
        self.memory[address] = value
        return self.memory[address]
