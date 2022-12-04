import pickle

opcodes = [
    ['halt', 0],
    ['set', 2],
    ['push', 1],
    ['pop', 1],
    ['eq', 3],
    ['gt', 3],
    ['jmp', 1],
    ['jt', 2],
    ['jf', 2],
    ['add', 3],
    ['mult', 3],
    ['mod', 3],
    ['and', 3],
    ['or', 3],
    ['not', 2],
    ['rmem', 2],
    ['wmem', 2],
    ['call', 1],
    ['ret', 0],
    ['out', 1],
    ['in', 1],
    ['noop', 0],
]

def save_vm(vm, filename):
    with open(filename, 'wb') as f:
        pickle.dump(vm, f)

def load_vm(old_vm, filename):

    with open(filename, 'rb') as f:
        vm = pickle.load(f)

        # TODO: display help output after loading
        vm.input_buffer = 'help\n'
        print('loaded')

        # This will stop the old VM but keep it in memory until all VMs are halted.
        # It's not optimal but good enough for this challenge.
        old_vm.halt = True
        vm.start()

class VM:
    program: bytearray
    ptr: int
    input_buffer: str
    stack: list[int]
    registers: list[int]
    halt: bool

    def __init__(self, program):
        self.program = program
        self.ptr = 0
        self.input_buffer = ''
        self.stack = []
        self.registers = [0] * 8
        self.halt = False

    def read_next_memory(self):
        low, high = self.program[self.ptr*2], self.program[self.ptr*2+1]
        self.ptr += 1
        return low + (high << 8)

    def read_memory(self, ptr: int) -> int:
        low, high = self.program[ptr*2], self.program[ptr*2+1]
        return low + (high << 8)

    def write_memory(self, ptr: int, mem: int) -> int:
        assert ptr*2+1 <= len(self.program)
        assert mem <= 32767
        self.program[ptr*2], self.program[ptr*2+1] = mem & 255, mem >> 8

    def read_register(self, i: int) -> int:
        return self.registers[i-32768]

    def write_register(self, i: int, value: int):
        self.registers[i-32768] = value

    def value(self, value: int) -> int:
        if value >= 32768:
            return self.read_register(value)
        else:
            return value

    def start(self):
        while not self.halt:
            op = self.read_next_memory()
            values = [self.read_next_memory() for i in range(0, opcodes[op][1])]
            self.exec(opcodes[op][0], values)

    def exec(self, op: str, values: list[int]):
        match op:
            case 'halt':
                self.halt = True
                return

            case 'set':
                self.write_register(values[0], self.value(values[1]))
            case 'push':
                self.stack.append(self.value(values[0]))
            case 'pop':
                self.write_register(values[0], self.stack.pop())

            case 'eq':
                if self.value(values[1]) == self.value(values[2]):
                    self.write_register(values[0], 1)
                else:
                    self.write_register(values[0], 0)
            case 'gt':
                if self.value(values[1]) > self.value(values[2]):
                    self.write_register(values[0], 1)
                else:
                    self.write_register(values[0], 0)

            case 'jmp':
                self.ptr = self.value(values[0])
            case 'jt':
                if self.value(values[0]) != 0:
                    self.ptr = values[1]
            case 'jf':
                if self.value(values[0]) == 0:
                    self.ptr = values[1]

            case 'add':
                res = self.value(values[1]) + self.value(values[2])
                self.write_register(values[0], res % 32768)
            case 'mult':
                res = self.value(values[1]) * self.value(values[2])
                self.write_register(values[0], res % 32768)
            case 'mod':
                res = self.value(values[1]) % self.value(values[2])
                self.write_register(values[0], res)

            case 'and':
                res = self.value(values[1]) & self.value(values[2])
                self.write_register(values[0], res)
            case 'or':
                res = self.value(values[1]) | self.value(values[2])
                self.write_register(values[0], res)
            case 'not':
                res = ~self.value(values[1]) % 32768
                self.write_register(values[0], res)

            case 'rmem':
                mem = self.read_memory(self.value(values[1]))
                self.write_register(values[0], mem)
            case 'wmem':
                self.write_memory(self.value(values[0]), self.value(values[1]))

            case 'call':
                self.stack.append(self.ptr)
                self.ptr = self.value(values[0])
            case 'ret':
                if len(self.stack) == 0:
                    self.halt = True
                    return
                self.ptr = self.stack.pop()

            case 'out':
                print(chr(self.value(values[0])), sep=' ', end='')
            case 'in':
                if len(self.input_buffer) == 0:
                    reading = True
                    while reading and not self.halt:
                        buf = input()
                        if len(buf) > 0 and buf[0] == '/':
                            self.special(buf)
                        else:
                            self.input_buffer = buf + '\n'
                            reading = False

                if not self.halt:
                    self.write_register(values[0], ord(self.input_buffer[0]))
                    self.input_buffer = self.input_buffer[1:]

            case 'noop':
                pass
            case _:
                print(f'not implemented: {op} {values}')
                self.halt = True
                return

    def special(self, command: str):
        cmd = command.split(' ')
        match cmd[0]:
            case '/quit':
                self.halt = True
            case '/save':
                save_vm(self, 'save.dat')
                print(f'saved. What do you do?')
            case '/load':
                load_vm(self, 'save.dat')
            case '/maze':
                print('go west, south, north')
            case '/coins':
                print('blue coin, red coin, shiny coin, concave coin, corroded coin')
            case '/exec':
                for op in opcodes:
                    if op[0] == cmd[1]:
                        if len(cmd[2:]) == op[1]:
                            print(f'exec: {cmd[1]} {cmd[2:]}')
                        else:
                            print(f'error: opcode {cmd[1]} requires {op[1]} parameters')
                        return
                print(f'error: opcode {cmd[1]} not found')
            case _:
                print(f'error: {cmd[0]} is not a command')

if __name__ == '__main__':
    with open('challenge.bin', 'rb') as f:
        program = bytearray(f.read())
    vm = VM(program)
    vm.start()
    print(f'vm done.\nstack: {vm.stack}\nregisters: {vm.registers}')

