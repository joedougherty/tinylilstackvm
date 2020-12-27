from cpu import CPU
from parser import parse_file


def test_addthem_exec():
    instructions = parse_file('code/addthem.bc')

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.stack.peek() == 3
