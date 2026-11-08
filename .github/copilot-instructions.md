# Copilot Instructions for python-6502-emulator

## Build, Test, and Lint Commands

- **Install dependencies:**
  - `python -m pip install --upgrade pip`
  - `python -m pip install tox-gh`
- **Run all tests:**
  - `tox r -e 3.14` (or `3.13`, `3.12`)
- **Run a single test file:**
  - `pytest tests/test_cpu.py` (or any test in `tests/`)
- **Run linting:**
  - `tox r -e lint`
- **Run code formatting/fix:**
  - `tox r -e fix`
- **Generate documentation:**
  - `tox r -e docs`

## High-Level Architecture

- The core emulator logic is in `src/m6502/`:
  - `processor.py`: Implements the 6502 CPU, registers, and instruction set.
  - `memory.py`: Implements 64KB addressable memory, including zero page and stack.
  - `__init__.py`: Exposes `Processor` and `Memory` classes.
- Tests are in `tests/`, covering CPU instructions and memory behavior.
- The project uses `pyproject.toml` for configuration and dependency management.
- Linting, formatting, and CI are managed via Tox and GitHub Actions.

## Key Conventions

- Python 3.12+ is required (see `pyproject.toml`).
- All source code is under `src/m6502/`.
- Tests use `pytest` and are located in `tests/`.
- Linting uses `flake8` (with plugins) and `yamllint`.
- Code formatting upgrades are automated with `pyupgrade` via the `fix` tox environment.
- Memory is always initialized to zero to avoid random data issues.
- The emulator is designed for clarity and educational value, with docstrings explaining 6502 concepts.

---

This file was generated to help Copilot and other AI tools understand the structure, workflows, and conventions of this repository. If you want to adjust or expand these instructions, let me know!
