"""
Stack Operations: PHA, PHP, PLA, PLP.

Tests for the 6502 CPU stack operation instructions:
- PHA (0x48): Push Accumulator
- PHP (0x08): Push Processor Status
- PLA (0x68): Pull Accumulator
- PLP (0x28): Pull Processor Status

Test Generation Patterns:
This module demonstrates scalable test parametrization using generators.
These patterns are reusable for other 6502 instructions like ADC, SBC, CMP, and
bit operations. By generating test data systematically, we achieve:
- Comprehensive coverage without manual duplication
- Easy extension to new instructions
- Reduction in test maintenance burden

Key generators:
- generate_boundary_byte_values(): Tests edge cases (0x00, 0x7F, 0x80, 0xFF)
- generate_single_flag_combinations(): Tests each flag individually
- generate_all_flag_combinations(): Tests all 128 flag combinations
"""

from typing import Generator

import pytest

from src.m6502 import Memory, Processor


# ============================================================================
# Test Data Generators
# ============================================================================
# These generators create parametrized test data systematically.
# They follow patterns useful for any 6502 instruction testing.


def generate_all_byte_values() -> Generator[int, None, None]:
    """Generate all possible 8-bit values (0x00-0xFF).

    Useful for exhaustive testing of instructions that operate on
    accumulator or memory values. For instructions like ADC, SBC, etc.

    Example usage:
        @pytest.mark.parametrize("value", generate_all_byte_values())
        def test_adc_all_byte_values(self, value: int) -> None: ...
    """
    yield from range(0x100)


def generate_boundary_byte_values() -> list[int]:
    """Generate boundary values for byte-sized operands.

    Returns: [zero, min_positive, max_positive, min_negative, max_negative, max]

    These are the critical edge cases for any 8-bit arithmetic or logic:
    - 0x00: Zero (both Z flag set/clear sensitivity)
    - 0x01: Minimum positive
    - 0x7F: Maximum positive (N flag boundary)
    - 0x80: Minimum negative (N flag boundary)
    - 0xFE: Maximum negative (nearly -1 in two's complement)
    - 0xFF: Maximum (-1 in two's complement)

    Example usage for future instructions:
        @pytest.mark.parametrize("value", generate_boundary_byte_values())
        def test_adc_boundary_values(self, value: int) -> None: ...
    """
    return [
        0x00,  # Zero
        0x01,  # Minimum positive
        0x7F,  # Maximum positive (bit 7 clear)
        0x80,  # Minimum negative (bit 7 set)
        0xFE,  # Maximum negative (nearly -1)
        0xFF,  # Maximum value (-1 in two's complement)
    ]


def generate_single_flag_combinations() -> list[tuple[int, bool, bool, bool, bool, bool, bool, bool]]:
    """Generate flag combinations with one flag set at a time.

    Returns list of tuples:
        (flags_byte, flag_c, flag_z, flag_i, flag_d, flag_b, flag_v, flag_n)

    Generates:
    - One case with all flags clear (0x00)
    - Seven cases with one flag set at a time
    - One case with all flags set (0xFE)

    Total: 9 test cases covering flag isolation.

    This pattern is useful for testing individual flag behavior in:
    - Flag push/pull operations (PHP, PLP)
    - Conditional branches (BNE, BEQ, BCC, etc.)
    - Flag-modifying instructions (SEC, CLC, etc.)

    Example usage:
        @pytest.mark.parametrize(
            ("flags_byte", "flag_c", "flag_z", "flag_i", "flag_d", "flag_b", "flag_v", "flag_n"),
            generate_single_flag_combinations(),
        )
        def test_instruction_flag_behavior(self, flags_byte, flag_c, ...): ...
    """
    combinations = []
    flag_bits = [
        (7, "Carry"),
        (6, "Zero"),
        (5, "Interrupt"),
        (4, "Decimal"),
        (3, "Break"),
        (2, "Overflow"),
        (1, "Negative"),
    ]

    # All flags clear case
    combinations.append((0x00, False, False, False, False, False, False, False))

    # Individual flag cases
    for bit_pos, _name in flag_bits:
        flags_byte = 1 << bit_pos
        flag_c = bool(flags_byte & (1 << 7))
        flag_z = bool(flags_byte & (1 << 6))
        flag_i = bool(flags_byte & (1 << 5))
        flag_d = bool(flags_byte & (1 << 4))
        flag_b = bool(flags_byte & (1 << 3))
        flag_v = bool(flags_byte & (1 << 2))
        flag_n = bool(flags_byte & (1 << 1))

        combinations.append((flags_byte, flag_c, flag_z, flag_i, flag_d, flag_b, flag_v, flag_n))

    # All flags set case
    combinations.append((0xFE, True, True, True, True, True, True, True))

    return combinations


def generate_all_flag_combinations() -> list[tuple[int, bool, bool, bool, bool, bool, bool, bool]]:
    """Generate ALL valid flag byte combinations (128 total).

    Returns list of tuples:
        (flags_byte, flag_c, flag_z, flag_i, flag_d, flag_b, flag_v, flag_n)

    This exhaustively tests all possible processor status configurations.
    Includes even/odd flag bytes (bit 0 is unused in 6502).

    Use this for comprehensive validation of flag preservation/modification,
    but be aware it generates 128 parametrized test cases.

    Example usage for very thorough testing:
        @pytest.mark.parametrize(
            ("flags_byte", "flag_c", "flag_z", "flag_i", "flag_d", "flag_b", "flag_v", "flag_n"),
            generate_all_flag_combinations(),
        )
        def test_flags_exhaustive(self, flags_byte, flag_c, ...): ...
    """
    combinations = []
    # Iterate through all possible flag combinations (2^7 = 128)
    # Step by 2 to skip bit 0 variations (unused in 6502)
    for flags_byte in range(0, 256, 2):
        flag_c = bool(flags_byte & (1 << 7))
        flag_z = bool(flags_byte & (1 << 6))
        flag_i = bool(flags_byte & (1 << 5))
        flag_d = bool(flags_byte & (1 << 4))
        flag_b = bool(flags_byte & (1 << 3))
        flag_v = bool(flags_byte & (1 << 2))
        flag_n = bool(flags_byte & (1 << 1))

        combinations.append((flags_byte, flag_c, flag_z, flag_i, flag_d, flag_b, flag_v, flag_n))

    return combinations


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def memory_and_cpu() -> tuple[Memory, Processor]:
    """Create a fresh memory and CPU for each test.

    Provides both a Memory instance and a reset Processor for convenient use.

    Example usage:
        def test_instruction(self, memory_and_cpu):
            memory, cpu = memory_and_cpu
            memory[cpu.PC_INIT] = 0x48  # PHA
            cpu.execute(3)
    """
    memory = Memory()
    cpu = Processor(memory)
    cpu.reset()
    return memory, cpu


# ============================================================================
# Push Accumulator (PHA) Tests
# ============================================================================


class TestPHA:
    """Push Accumulator (PHA - 0x48) instruction tests.

    Tests that PHA correctly pushes the accumulator value onto the stack
    without modifying flags, and handles stack pointer wraparound.
    """

    def test_pha_basic_push(self) -> None:
        """Test basic PHA operation with a known value."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.reg_a = 0x42
        memory[Processor.PC_INIT] = 0x48  # PHA opcode

        cpu.execute(3)

        assert (
            cpu.program_counter,
            cpu.stack_pointer,
            cpu.cycles,
            memory[0x01FD],  # Value pushed to stack
        ) == (0xFCE3, 0x01FC, 3, 0x42)

    @pytest.mark.parametrize("value", generate_boundary_byte_values())
    def test_pha_boundary_values(self, value: int) -> None:
        """Test PHA with boundary byte values using scalable generator.

        Uses generate_boundary_byte_values() to parametrize systematically
        instead of hand-writing test cases. This pattern scales to any
        instruction testing byte values (ADC, LDA, SBC, etc.).

        Covers: 0x00, 0x01, 0x7F, 0x80, 0xFE, 0xFF
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.reg_a = value
        memory[Processor.PC_INIT] = 0x48

        cpu.execute(3)

        assert memory[0x01FD] == value
        assert cpu.stack_pointer == 0x01FC

    def test_pha_stack_pointer_wraparound(self) -> None:
        """Test PHA when stack pointer wraps from 0x0100 to 0x01FF."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.stack_pointer = 0x0100  # Wrap to 0x01FF
        cpu.reg_a = 0xAA
        memory[Processor.PC_INIT] = 0x48

        cpu.execute(3)

        assert memory[0x0100] == 0xAA
        assert cpu.stack_pointer == 0x01FF

    def test_pha_does_not_affect_flags(self) -> None:
        """Test that PHA does not modify any processor flags."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.reg_a = 0x42
        memory[Processor.PC_INIT] = 0x48

        # Set various flag states
        cpu.flag_c = False
        cpu.flag_z = False
        cpu.flag_n = True
        cpu.flag_v = True

        initial_flags = (
            cpu.flag_c,
            cpu.flag_z,
            cpu.flag_n,
            cpu.flag_v,
            cpu.flag_i,
            cpu.flag_d,
            cpu.flag_b,
        )

        cpu.execute(3)

        final_flags = (
            cpu.flag_c,
            cpu.flag_z,
            cpu.flag_n,
            cpu.flag_v,
            cpu.flag_i,
            cpu.flag_d,
            cpu.flag_b,
        )

        assert initial_flags == final_flags


# ============================================================================
# Push Processor Status (PHP) Tests
# ============================================================================


class TestPHP:
    """Push Processor Status (PHP - 0x08) instruction tests.

    Tests that PHP correctly encodes and pushes the processor status flags
    with the correct bit layout onto the stack.

    Flag byte layout:
        Bit 7: Carry (C)
        Bit 6: Zero (Z)
        Bit 5: Interrupt Disable (I)
        Bit 4: Decimal Mode (D)
        Bit 3: Break Command (B)
        Bit 2: Overflow (V)
        Bit 1: Negative (N)
        Bit 0: (unused - always 0)
    """

    def test_php_all_flags_set(self) -> None:
        """Test PHP with all flags set."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.flag_c = True
        cpu.flag_z = True
        cpu.flag_i = True
        cpu.flag_d = True
        cpu.flag_b = True
        cpu.flag_v = True
        cpu.flag_n = True
        memory[Processor.PC_INIT] = 0x08  # PHP opcode

        cpu.execute(3)

        assert (cpu.program_counter, cpu.stack_pointer, cpu.cycles) == (0xFCE3, 0x01FC, 3)
        assert memory[0x01FD] == 0xFE  # All bits set except bit 0

    def test_php_no_flags_set(self) -> None:
        """Test PHP with all flags clear."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.flag_c = False
        cpu.flag_z = False
        cpu.flag_i = False
        cpu.flag_d = False
        cpu.flag_b = False
        cpu.flag_v = False
        cpu.flag_n = False
        memory[Processor.PC_INIT] = 0x08

        cpu.execute(3)

        assert memory[0x01FD] == 0x00

    @pytest.mark.parametrize(
        ("flags_byte", "flag_c", "flag_z", "flag_i", "flag_d", "flag_b", "flag_v", "flag_n"),
        generate_single_flag_combinations(),
    )
    def test_php_flag_combinations(
        self,
        flags_byte: int,
        flag_c: bool,
        flag_z: bool,
        flag_i: bool,
        flag_d: bool,
        flag_b: bool,
        flag_v: bool,
        flag_n: bool,
    ) -> None:
        """Test PHP with various flag combinations using generator.

        Uses generate_single_flag_combinations() for systematic testing.
        Each parametrized case tests a unique flag pattern (9 total).

        This pattern scales to testing conditions with multiple flags,
        like in branch instructions (BNE, BEQ, BCC, etc.) or ADC/SBC
        overflow detection.

        Covers:
        - All flags clear
        - One flag set at a time (7 cases)
        - All flags set
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        cpu.flag_c = flag_c
        cpu.flag_z = flag_z
        cpu.flag_i = flag_i
        cpu.flag_d = flag_d
        cpu.flag_b = flag_b
        cpu.flag_v = flag_v
        cpu.flag_n = flag_n
        memory[Processor.PC_INIT] = 0x08

        cpu.execute(3)

        assert memory[0x01FD] == flags_byte


# ============================================================================
# Pull Accumulator (PLA) Tests
# ============================================================================


class TestPLA:
    """Pull Accumulator (PLA - 0x68) instruction tests.

    Tests that PLA correctly retrieves a value from the stack into the
    accumulator and sets the Zero and Negative flags appropriately.
    """

    def test_pla_basic_pull(self) -> None:
        """Test basic PLA operation pulling a value from stack."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x68  # PLA opcode
        memory[0x01FE] = 0x42  # Value on stack (will be read after SP increment)
        cpu.reg_a = 0x00

        cpu.execute(4)

        assert (
            cpu.program_counter,
            cpu.stack_pointer,
            cpu.cycles,
            cpu.reg_a,
        ) == (0xFCE3, 0x01FE, 4, 0x42)

    @pytest.mark.parametrize("value", generate_boundary_byte_values())
    def test_pla_boundary_values(self, value: int) -> None:
        """Test PLA with boundary values and flag effects.

        Uses generate_boundary_byte_values() to systematically test
        how different values set/clear the Z and N flags.

        Boundary values ensure we test:
        - Zero (Z flag)
        - Sign bit boundary (N flag)
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x68
        memory[0x01FE] = value  # Value at SP+1 (will be read after increment)

        cpu.execute(4)

        assert cpu.reg_a == value
        assert cpu.flag_z == (value == 0x00)
        assert cpu.flag_n == bool(value & 0x80)

    def test_pla_stack_pointer_increment(self) -> None:
        """Test that PLA increments the stack pointer."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        initial_sp = cpu.stack_pointer
        memory[Processor.PC_INIT] = 0x68
        memory[initial_sp + 1] = 0x42  # Value at SP+1 (will be read after increment)

        cpu.execute(4)

        assert cpu.stack_pointer == initial_sp + 1

    def test_pla_zero_flag_behavior(self) -> None:
        """Test PLA sets Zero flag correctly."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x68
        memory[0x01FE] = 0x00

        cpu.execute(4)

        assert cpu.flag_z is True
        assert cpu.reg_a == 0x00

    def test_pla_negative_flag_behavior(self) -> None:
        """Test PLA sets Negative flag when bit 7 is set."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x68
        memory[0x01FE] = 0x80

        cpu.execute(4)

        assert cpu.flag_n is True
        assert cpu.reg_a == 0x80


# ============================================================================
# Pull Processor Status (PLP) Tests
# ============================================================================


class TestPLP:
    """Pull Processor Status (PLP - 0x28) instruction tests.

    Tests that PLP correctly retrieves a flag byte from the stack and
    restores all processor status flags.

    Flag byte layout (matches PHP push format):
        Bit 7: Carry (C)
        Bit 6: Zero (Z)
        Bit 5: Interrupt Disable (I)
        Bit 4: Decimal Mode (D)
        Bit 3: Break Command (B)
        Bit 2: Overflow (V)
        Bit 1: Negative (N)
        Bit 0: (unused - ignored)
    """

    def test_plp_all_flags_set(self) -> None:
        """Test PLP with all flags set in the flag byte."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x28  # PLP opcode
        memory[0x01FE] = 0xFE  # All flags set except bit 0

        cpu.execute(4)

        assert (cpu.program_counter, cpu.stack_pointer, cpu.cycles) == (0xFCE3, 0x01FE, 4)
        assert (
            cpu.flag_c,
            cpu.flag_z,
            cpu.flag_i,
            cpu.flag_d,
            cpu.flag_b,
            cpu.flag_v,
            cpu.flag_n,
        ) == (True, True, True, True, True, True, True)

    def test_plp_no_flags_set(self) -> None:
        """Test PLP with no flags set in the flag byte."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x28
        memory[0x01FE] = 0x00

        cpu.execute(4)

        assert (
            cpu.flag_c,
            cpu.flag_z,
            cpu.flag_i,
            cpu.flag_d,
            cpu.flag_b,
            cpu.flag_v,
            cpu.flag_n,
        ) == (False, False, False, False, False, False, False)

    @pytest.mark.parametrize(
        ("flags_byte", "flag_c", "flag_z", "flag_i", "flag_d", "flag_b", "flag_v", "flag_n"),
        generate_single_flag_combinations(),
    )
    def test_plp_flag_combinations(
        self,
        flags_byte: int,
        flag_c: bool,
        flag_z: bool,
        flag_i: bool,
        flag_d: bool,
        flag_b: bool,
        flag_v: bool,
        flag_n: bool,
    ) -> None:
        """Test PLP with various flag combinations using generator.

        Uses generate_single_flag_combinations() to systematically
        test each flag individually, plus all-set and all-clear cases.

        This pattern is essential for testing instructions that modify
        flags (ADC overflow, shift carry, comparisons, etc.) where we
        need to verify that ONLY the intended flags change.
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        memory[Processor.PC_INIT] = 0x28
        memory[0x01FE] = flags_byte

        cpu.execute(4)

        assert (
            cpu.flag_c,
            cpu.flag_z,
            cpu.flag_i,
            cpu.flag_d,
            cpu.flag_b,
            cpu.flag_v,
            cpu.flag_n,
        ) == (flag_c, flag_z, flag_i, flag_d, flag_b, flag_v, flag_n)

    def test_plp_stack_pointer_increment(self) -> None:
        """Test that PLP increments the stack pointer."""
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()
        initial_sp = cpu.stack_pointer
        memory[Processor.PC_INIT] = 0x28
        memory[initial_sp] = 0x00  # Value at current SP

        cpu.execute(4)

        assert cpu.stack_pointer == initial_sp + 1


# ============================================================================
# Sequence Tests (Integration)
# ============================================================================


class TestStackSequences:
    """Test sequences of stack operations to verify round-trip behavior.

    Integration tests that verify push-pull pairs work correctly together.
    """

    def test_pha_pla_roundtrip(self) -> None:
        """Test that PHA followed by PLA preserves accumulator value.

        Demonstrates a common stack pattern: save-restore of A register.
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()

        # PHA: Push 0x42
        cpu.reg_a = 0x42
        memory[0xFCE2] = 0x48  # PHA
        # PLA: Pull into A
        memory[0xFCE3] = 0x68  # PLA

        initial_a = cpu.reg_a
        initial_sp = cpu.stack_pointer
        cpu.execute(7)  # 3 cycles for PHA + 4 cycles for PLA

        assert cpu.reg_a == initial_a
        assert cpu.stack_pointer == initial_sp

    def test_php_plp_roundtrip(self) -> None:
        """Test that PHP followed by PLP preserves processor status.

        Demonstrates a common pattern: save-restore of processor status
        for interrupt handlers or context switching.
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()

        # Set up some flags
        cpu.flag_c = True
        cpu.flag_z = False
        cpu.flag_n = True
        cpu.flag_d = False

        # PHP: Push flags
        memory[0xFCE2] = 0x08  # PHP
        # PLP: Pull flags
        memory[0xFCE3] = 0x28  # PLP

        initial_flags = (cpu.flag_c, cpu.flag_z, cpu.flag_n, cpu.flag_d)
        initial_sp = cpu.stack_pointer
        cpu.execute(7)  # 3 cycles for PHP + 4 cycles for PLP

        final_flags = (cpu.flag_c, cpu.flag_z, cpu.flag_n, cpu.flag_d)
        assert initial_flags == final_flags
        assert cpu.stack_pointer == initial_sp

    def test_multiple_pha_operations(self) -> None:
        """Test multiple sequential PHA operations.

        Demonstrates stack depth: pushing multiple values creates a
        stack frame.
        """
        memory = Memory()
        cpu = Processor(memory)
        cpu.reset()

        initial_sp = cpu.stack_pointer

        # Push three values one at a time
        values = [0x11, 0x22, 0x33]
        for i, value in enumerate(values):
            cpu.reg_a = value
            memory[0xFCE2 + i] = 0x48  # PHA
            # Execute just this one instruction (3 cycles total)
            cpu.execute(cpu.cycles + 3)

        # Check stack has all values in reverse order (LIFO)
        assert memory[0x01FD] == 0x11  # First pushed
        assert memory[0x01FC] == 0x22
        assert memory[0x01FB] == 0x33  # Last pushed
        assert cpu.stack_pointer == initial_sp - 3


# ============================================================================
# Documentation: Adding Tests for New Instructions
# ============================================================================
# When implementing a new 6502 instruction (like ADC, SBC, CMP), reuse
# these generator patterns:
#
# For value-based instructions (ADC, SBC, ORA, AND, EOR, CMP, etc.):
#   @pytest.mark.parametrize("value", generate_boundary_byte_values())
#   def test_instruction_value_behavior(self, value: int) -> None: ...
#
# For flag-affecting instructions (SEC, CLC, SEI, CLI, etc.):
#   @pytest.mark.parametrize(
#       ("flags_byte", "flag_c", "flag_z", ...),
#       generate_single_flag_combinations(),
#   )
#   def test_instruction_flag_effect(self, flags_byte, flag_c, ...): ...
#
# For exhaustive testing of edge cases in arithmetic:
#   @pytest.mark.parametrize("value", generate_all_byte_values())
#   def test_adc_all_values(self, value: int) -> None: ...
#
# For comprehensive flag testing (less common, 128 cases):
#   @pytest.mark.parametrize(
#       ("flags_byte", "flag_c", ...),
#       generate_all_flag_combinations(),
#   )
#   def test_instruction_exhaustive_flags(self, flags_byte, ...): ...
