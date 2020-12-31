def parse_program(fname):
    lines = raw_lines(fname)
    instructions = process_lines(lines)
    symbol_table = generate_symbol_table(instructions)
    linked_instructions = link(instructions, symbol_table)
    return linked_instructions


def raw_lines(fname):
    with open(fname) as f:
        file_contents = f.readlines()
    return file_contents


def process_lines(file_contents):
    instructions = []
    for line in file_contents:
        instructions += parse_line(line)

    return instructions


def parse_line(line):
    agg = []
    line = line.replace('\t', ' ')
    for token in line.split(' '):
        token = token.strip('\n')

        if token != '#':
            if token.isnumeric():
                parsed_token = int(token)
            else:
                parsed_token = token 

            if parsed_token not in ('', ' '):
                agg.append(parsed_token)
        else:
            # Everything from '#' to EOL is a comment -- skip it
            break
    return agg


def link(instructions, symbol_table):
    resolved_instructions = []
    for inst in instructions:
        if inst in symbol_table.keys():
            resolved_instructions.append(symbol_table[inst])
        else:
            resolved_instructions.append(inst)

    return resolved_instructions
            

def generate_symbol_table(instructions):
    symbol_table = dict()
    for idx, elem in enumerate(instructions):
        if isinstance(elem, str) and elem.endswith(':'):
            symbol_table[elem.strip(':')] = idx 

    return symbol_table
