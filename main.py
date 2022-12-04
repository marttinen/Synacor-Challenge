import sys

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

stack = []
registers = [0] * 8

def read(program: bytearray, ptr: int) -> int:
    assert ptr*2+1 <= len(program)
    low, high = program[ptr*2], program[ptr*2+1]
    return low + (high << 8)

def write(program: bytearray, ptr: int, mem: int) -> int:
    assert ptr*2+1 <= len(program)
    assert mem <= 32767
    program[ptr*2], program[ptr*2+1] = mem & 255, mem >> 8

def register(num: int) -> int:
    return num-32768

def get_value(val: int) -> int:
    if val >= 32768:
        return registers[register(val)]
    else:
        return val

def main(program: bytearray):
    ptr = 0
    input_buffer = ''
    while True:
        op = read(program, ptr)
        ptr += 1
        code = opcodes[op]
        values = [read(program, ptr+i) for i in range(0, code[1])]
        ptr += code[1]

        match code[0]:
            case 'halt':
                return

            case 'set':
                registers[register(values[0])] = get_value(values[1])
            case 'push':
                stack.append(get_value(values[0]))
            case 'pop':
                registers[register(values[0])] = stack.pop()

            case 'eq':
                if get_value(values[1]) == get_value(values[2]):
                    registers[register(values[0])] = 1
                else:
                    registers[register(values[0])] = 0
            case 'gt':
                if get_value(values[1]) > get_value(values[2]):
                    registers[register(values[0])] = 1
                else:
                    registers[register(values[0])] = 0

            case 'jmp':
                ptr = get_value(values[0])
            case 'jt':
                if get_value(values[0]) != 0:
                    ptr = values[1]
            case 'jf':
                if get_value(values[0]) == 0:
                    ptr = values[1]

            case 'add':
                res = get_value(values[1]) + get_value(values[2])
                registers[register(values[0])] = res % 32768
            case 'mult':
                res = get_value(values[1]) * get_value(values[2])
                registers[register(values[0])] = res % 32768
            case 'mod':
                res = get_value(values[1]) % get_value(values[2])
                registers[register(values[0])] = res

            case 'and':
                registers[register(values[0])] = get_value(values[1]) & get_value(values[2])
            case 'or':
                registers[register(values[0])] = get_value(values[1]) | get_value(values[2])
            case 'not':
                registers[register(values[0])] = ~get_value(values[1]) % 32768

            case 'rmem':
                mem = read(program, get_value(values[1]))
                registers[register(values[0])] = mem
            case 'wmem':
                write(program, get_value(values[0]), get_value(values[1]))

            case 'call':
                stack.append(ptr)
                ptr = get_value(values[0])
            case 'ret':
                if len(stack) == 0: return
                ptr = stack.pop()

            case 'out':
                print(chr(get_value(values[0])), sep=' ', end='')
            case 'in':
                if len(input_buffer) == 0:
                    input_buffer = input() + '\n'

                registers[register(values[0])] = ord(input_buffer[0])
                input_buffer = input_buffer[1:]

            case 'noop':
                pass
            case _:
                print(f'not implemented: {code} {values}')
                return

if __name__ == '__main__':
    with open('challenge.bin', 'rb') as f:
        program = bytearray(f.read())
        main(program)
        print(f'program done.\nstack: {stack}\nregisters: {registers}')

