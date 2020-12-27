from cpu import CPU


def test_empty_program_does_nothing():
    instructions = ["HALT"]

    cpu = CPU(instructions)
    cpu.step()

    assert cpu.halted == True
    assert cpu.instruction_address == 1
    assert cpu.stack.is_empty() == True


def test_push_push_and_then_halt():
    instructions = ["PUSH", 42, "PUSH", 68, "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 5
    assert cpu.stack[-1] == 68
    assert cpu.stack[-2] == 42


def test_add_two_numbers():
    instructions = ["PUSH", 1, "PUSH", 2, "ADD", "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 6
    assert cpu.stack[-1] == 3


def test_sub_two_numbers():
    instructions = ["PUSH", 1, "PUSH", 2, "SUB", "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 6
    assert cpu.stack[-1] == -1


def test_unary_not_true():
    instructions = ["PUSH", 1, "NOT", "HALT"]
    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 4
    assert cpu.stack[-1] == 0


def test_unary_not_false():
    instructions = ["PUSH", 0, "NOT", "HALT"]
    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 4
    assert cpu.stack[-1] == 1


def test_and_true_true():
    instructions = ["PUSH", 1, "PUSH", 1, "AND", "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 6
    assert cpu.stack[-1] == 1


def test_or_true_false():
    instructions = ["PUSH", 1, "PUSH", 0, "OR", "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 6
    assert cpu.stack[-1] == 1


def test_pop():
    instructions = ["PUSH", 42, "POP", "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 4
    assert cpu.stack.is_empty() == True


def test_dup():
    instructions = ["PUSH", 42, "DUP", "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 4
    assert cpu.stack[-1] == 42
    assert cpu.stack[-2] == 42


def test_unconditional_jump():
    # address:       0     1   2       3     4
    instructions = ["JMP", 3, "HALT", "JMP", 2]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 3


def test_conditional_jump():
    # address:      0       1   2     3   4      5      6   7     8   9
    instructions = ["PUSH", 1, "JIF", 5, "POP", "PUSH", 0, "JIF", 4, "HALT"]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.instruction_address == 10

def test_if_else_block():
    '''

    if (a > b) {
        c = a;
    } else {
        c = b;
    }

    '''
    instructions = [
        # Init a with "6"
        'PUSH', 6,
        'STORE', 0,
        
        # Init b with "4"
        'PUSH', 4,
        'STORE', 1,
        
        # Load a and b into the stack
        'LOAD', 0,            # Stack contains a
        'LOAD', 1,            # Stack contains a, b
        'ISGT',               # Stack contains a > b
        'JIF', 21,
        
        # This is the "else" path
        'LOAD', 1,            # Stack contains b
        'STORE', 2,           # Set c to the stack head, meaning c = b
        'JMP', 25,
        
        # This is the "if" path, and this is the address 21
        'LOAD', 0,            # Stack contains a
        'STORE', 2,           # Set c to the stack head, meaning c = a
        
        # Done; this is address 25
        'HALT'
    ]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    current_frame = cpu.frame_stack.peek()
    assert current_frame[2] == 6


def test_while_block():
    '''
    
    a = 6;
    b = 4;
    total = 0;

    while (b >= 1) {
        total += a;
        --b;
    }


    '''
    instructions = [
        # Init a with "6"
        "PUSH", 6,
        "STORE", 0,

        # Init b with "4"
        "PUSH", 4,
        "STORE", 1,

        # Init total to 0
        "PUSH", 0,
        "STORE", 2,

        # While part
        # Here is address 12
        "LOAD", 1,            # Stack contains b
        "PUSH", 1,            # Stack contains b, 1
        "ISGE",               # Stack contains b >= 1
        "NOT",                # Stack contains b < 1
        "JIF", 36,            # 36 is the address of the "HALT" label

        # Inner loop part
        "LOAD", 0,            # Stack contains a
        "LOAD", 2,            # Stack contains a, total
        "ADD",                # Stack contains a + total
        "STORE", 2,           # Save in total, meaning total = a + total

        "LOAD", 1,            # Stack contains b
        "PUSH", 1,            # Stack contains b, 1
        "SUB",                # Stack contains b - 1
        "STORE", 1,           # Save in b, meaning b = b - 1

        "JMP", 12,            # Go back to the start of the loop

        "HALT"
    ]
    
    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    
    current_frame = cpu.frame_stack.peek()

    assert current_frame[0] == 6    # a = 6
    assert current_frame[1] == 0    # b = 0
    assert current_frame[2] == 24   # total = 24

def test_max_function():
    '''
    int max(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    '''

    instructions = [
        "PUSH", 6,        # Push the first argument
        "PUSH", 4,        # Push the second argument
        "CALL", 7,        # Call "max"
        "HALT",

        # Here is address 7, the start of "max" function
        "STORE", 1,       # Store b in local variable 1; the stack now contains [a]
        "STORE", 0,       # Store a in local variable 0; the stack is now empty
        "LOAD", 0,        # The stack now contains [a]
        "LOAD", 1,        # The stack now contains [a, b]
        "ISGE",           # The stack now contains [a > b]
        "JIF", 21,        # If the top of the stack is true (a > b), jump to the "if" path
        "LOAD", 1,        # "else" path: load b on the stack
        "RET",

        # Here is address 23
        "LOAD", 0,        # "if" path: load a on the stack
        "RET"
    ]

    cpu = CPU(instructions)
    cpu.run()

    assert cpu.halted == True
    assert cpu.stack.peek() == 6
    assert cpu.instruction_address == 7 
