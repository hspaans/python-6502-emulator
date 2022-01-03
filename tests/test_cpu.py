"""Verifies that the processor class works as expected."""
import m6502


def test_cpu_reset() -> None:
    """Verify CPU state after CPU Reset.

    :return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.flag_b,
        cpu.flag_d,
        cpu.flag_i
    ) == (
        0xFCE2,
        0x01FD,
        True,
        False,
        True
    )
