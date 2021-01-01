from cpu import CPU
from tinylilparser import parse_program


def test_addthem_exec():
    instructions = parse_program('code/addthem.bc')

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.stack.peek() == 3


def test_maxfun_exec():
    instructions = parse_program('code/maxfun.bc')

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.stack.peek() == 6


def test_countdown_exec():
    instructions = parse_program('code/countdown.bc')

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True


def test_noop_exec():
    instructions = parse_program('code/noop.bc')

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.steps == 1
