from bc_parser import parse_file, parse_line


def test_maxfun_bc():
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

    assert instructions == parse_file('code/maxfun.bc')

