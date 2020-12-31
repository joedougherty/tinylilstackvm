from tinylilparser import parse_program


def test_maxfun_bc():
    instructions = [
        'PUSH', 6,
        'PUSH', 4,
        'CALL', 7,
        'HALT',
        'MAX:',
        'STORE', 1,
        'STORE', 0,
        'LOAD',  0,
        'LOAD',  1,
        'ISGE',
        'JIF',   22,
        'LOAD',  1,
        'RET',
        'ENDMAX:',
        'LOAD',  0,
        'RET'
    ]

    assert instructions == parse_program('code/maxfun.bc')

