def parse_file(fname):
    with open(fname) as f:
        file_contents = f.readlines()
    
    instructions = []
    for line in file_contents:
        instructions += parse_line(line)

    return link(instructions)


def parse_line(l):
    agg = []
    for token in l.split(' '):
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


### LINKING ###
def link(instructions):
    while index_label(instructions) != dict():
        instructions = resolve_label(instructions, index_label(instructions))
    return instructions


def resolve_label(instructions, label_index):
    agg = []
    for elem in instructions:
        elem_c = f'''{elem}:'''
        if isinstance(elem, str) and elem in label_index.keys():
            agg.append(label_index[elem])
        elif isinstance(elem, str) and elem.endswith(':'):
            continue
        else:
            agg.append(elem)
    return agg


def index_label(insts):
    label_index = dict()
    for idx, item in enumerate(insts):
        if isinstance(item, str) and item.endswith(':'):
            label_index[item.strip(':')] = idx
            return label_index

    return dict()
