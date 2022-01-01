import m6502


def test_cpu_reset() -> None:
    """Verify CPU state after CPU Reset"""
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    assert (cpu.program_counter, cpu.stack_pointer, cpu.flag_d) == (0xFFFC, 0x0100, False)
