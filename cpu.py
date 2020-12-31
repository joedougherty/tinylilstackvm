"""

https://andreabergia.com/stack-based-virtual-machines-2/

  - HALT
  - PUSH
  - ADD

https://andreabergia.com/stack-based-virtual-machines-3/

  - SUB
  - MUL
  - DIV
  - NOT
  - AND
  - OR 

https://andreabergia.com/stack-based-virtual-machines-4/

  - ISEQ
  - ISGE
  - ISGT
  - JMP
  - JIF
  - STORE
  - LOAD

https://andreabergia.com/stack-based-virtual-machines-5/

    ???

https://andreabergia.com/stack-based-virtual-machines-6/

  - CALL
  - RET

"""


class StackUnderflowError(Exception):
    pass


class RunTimeError(Exception):
    pass


class Stack:
    def __init__(self):
        self.contents = []

    def push(self, v):
        self.contents.append(v)

    def peek(self, idx=-1):
        return self.contents[idx]

    def pop(self):
        return self.contents.pop()

    def is_empty(self):
        return len(self.contents) == 0

    def height(self):
        return len(self.contents)

    def __getitem__(self, i):
        return self.contents[i]

    def __setitem__(self, i, value):
        self.contents[i] = value


class Frame:
    def __init__(self, return_address):
        self.return_address = return_address
        self.contents = dict()

    def __setitem__(self, k, v):
        self.contents[k] = v

    def __getitem__(self, k):
        return self.contents[k]


class CPU:
    def __init__(self, instructions):
        self.program = instructions
        self.instruction_address = 0
        self.stack = Stack()
        self.halted = False

        self.frame_stack = Stack()
        self.frame_stack.push(Frame(0))

        self.builtin_ops = {
            "HALT": self.halt,
            "PUSH": self.push,
            "POP": self.pop,
            "DUP": self.dup,
            "ROT": self.rotate,
            "OVER": self.over,
            "NOT": self._not,
            "AND": self._and,
            "OR": self._or,
            "ADD": self.add,
            "SUB": self.sub,
            "MUL": self.mul,
            "DIV": self.div,
            "ISEQ": self.iseq,
            "ISGE": self.isge,
            "ISGT": self.isgt,
            "JMP": self.jmp,
            "JIF": self.jif,
            "STORE": self.store,
            "LOAD": self.load,
            "CALL": self._call,
            "RET": self._return,
        }

    def get_next_word_from_program(self, err_msg=""):
        print(self.instruction_address)
        print(len(self.program))
        if self.instruction_address >= len(self.program):
            raise RunTimeError(err_msg)

        next_word = self.program[self.instruction_address]
        self.instruction_address += 1
        return next_word

    def decode_instruction(self, instruction):
        if instruction not in self.builtin_ops:
            raise RunTimeError(f"""Unknown instruction: {instruction}""")

        op = self.builtin_ops.get(instruction)
        op()

    def _unary_op_arg(self, op=""):
        if self.stack.height() < 1:
            if op:
                msg = f"""Not enough items on stack for operation: {op}"""
            else:
                msg = f"""Not enough items on stack"""

            raise StackUnderflowError(msg)

        return self.stack.pop()

    def push(self):
        value = self.get_next_word_from_program(
            err_msg="""Should have the value after the PUSH instruction"""
        )
        self.stack.push(value)

    def pop(self):
        return self._unary_op_arg("POP")

    def dup(self):
        self.stack.push(self.stack.peek())

    def rotate(self):
        c, b, a = self.stack.pop(), self.stack.pop(), self.stack.pop()
        self.stack.push(b)
        self.stack.push(a)
        self.stack.push(c)

    def over(self):
        self.stack.push(self.stack.peek[-2])

    def _binary_op_args(self, op=""):
        if self.stack.height() < 2:
            if op:
                msg = f"""Not enough items on stack for operation: {op}"""
            else:
                msg = f"""Not enough items on stack"""

            raise StackUnderflowError(msg)

        return (self.stack.pop(), self.stack.pop())

    def add(self):
        a, b = self._binary_op_args("ADD")
        self.stack.push(b + a)

    def sub(self):
        a, b = self._binary_op_args("SUB")
        self.stack.push(b - a)

    def mul(self):
        a, b = self._binary_op_args("MUL")
        self.stack.push(b * a)

    def div(self):
        a, b = self._binary_op_args("DIV")
        self.stack.push(b // a)

    def _not(self):
        tos = self._unary_op_arg("NOT")
        inverted_tos = not bool(tos)
        self.stack.push(int(inverted_tos))

    def _and(self):
        a, b = self._binary_op_args("AND")
        self.stack.push(int(bool(a) and bool(b)))

    def _or(self):
        a, b = self._binary_op_args("OR")
        self.stack.push(int(bool(a) or bool(b)))

    def iseq(self):
        a, b = self._binary_op_args("ISEQ")
        self.stack.push(int(a == b))

    def isge(self):
        a, b = self._binary_op_args("ISGE")
        self.stack.push(int(b >= a))

    def isgt(self):
        a, b = self._binary_op_args("ISGT")
        self.stack.push(int(b > a))

    def jmp(self):
        address = self.get_next_word_from_program(
            err_msg="""Should have an address to jump to"""
        )
        self.instruction_address = address

    def jif(self):
        address = self.get_next_word_from_program(
            err_msg="""Should have an address to jump to"""
        )
        if bool(self.stack.pop()) == True:
            self.instruction_address = address

    def load(self):
        current_frame = self.frame_stack.peek()
        loc = self.get_next_word_from_program(err_msg="""Should have loc for LOAD""")
        self.stack.push(current_frame[loc])

    def store(self):
        current_frame = self.frame_stack.peek()
        loc = self.get_next_word_from_program(err_msg="""Should have loc for STORE""")
        current_frame[loc] = self.stack.pop()

    def _call(self):
        address = self.get_next_word_from_program(err_msg="""Should have an address for CALL""")
        self.frame_stack.push(Frame(self.instruction_address))
        self.instruction_address = address

    def _return(self):
        current_frame = self.frame_stack.peek()
        return_address = current_frame.return_address
        self.frame_stack.pop()
        self.instruction_address = return_address

    def step(self):
        if self.halted:
            raise RuntTimeError("Cannot step while halted")

        next_instruction = self.get_next_word_from_program(
            err_msg="""Should have a next instruction"""
        )
        self.decode_instruction(next_instruction)

    def run(self):
        while not self.halted:
            self.step()
