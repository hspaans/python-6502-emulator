"""Emulation of the MOT-6502 memory."""


class Memory:
    """
    Memory bank for 6502 systems.

    The memory is by default 64KB in size and is addressed from 0x0000 to
    0xFFFF. The memory is initialized with all zeros to reduce the chance of
    random data causing issues.
    """

    def __init__(self, size: int = 0xFFFF) -> None:
        """
        Initialize the memory.

        :param int size: The size of the memory
        :raises ValueError: Memory size is not valid
        """
        if size is None:
            size = 0xFFFF
        if size < 0x0200:
            raise ValueError("Memory size is not valid")
        if size > 0xFFFF:
            raise ValueError("Memory size is not valid")
        self.size = size
        self.memory = [0] * self.size

    def __getitem__(self, address: int) -> int:
        """
        Get the value at the specified memory address.

        :param int address: The memory address to read from
        :return: The value at the specified address
        :rtype: int
        :raises ValueError: Memory address is not valid
        """
        if 0x0000 < address > self.size:
            raise ValueError("Memory address is not valid")
        return self.memory[address]

    def __setitem__(self, address: int, value: int) -> int:
        """
        Set the value at the specified memory address.

        :param int address: The address to write to
        :param int value: The value to write to the address
        :return: The value written to the specified memory address
        :rtype: int
        :raises ValueError: Memory address is not valid
        :raises ValueError: Size of value exceed byte size
        """
        if 0x0000 < address > self.size:
            raise ValueError("Memory address is not valid")
        if value.bit_length() > 8:
            raise ValueError("Value too large")
        self.memory[address] = value
        return self.memory[address]
