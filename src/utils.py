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

def save_vm(vm):
    with open('save.bin', 'wb') as f:
        pickle.dump(vm, f)

def load_vm(old_vm):
    with open('save.bin', 'rb') as f:
        vm = pickle.load(f)

        print('loaded, try looking around...')
        # TODO: display look after loading
        vm.input_buffer = '\n'

        # This will stop the old VM but keep it in memory until all VMs are halted.
        # It's not optimal but good enough for this challenge.
        old_vm.halt = True
        vm.start()

def dump_vm(vm):
    with open('program.asm', 'w') as f:
        ptr = 0
        while vm.has_memory_address(ptr):
            f.write(f'{ptr:05}:    ')
            op, ptr = vm.read_memory(ptr), ptr+1

            if op < len(opcodes):
                values = [translate_value(vm.read_memory(ptr+i)) for i in range(0, opcodes[op][1])]
                ptr += len(values)
                f.write(f'{opcodes[op][0]:>4}    {" ".join(values)}\n')
            else:
                f.write(f'        {translate_value(op)}\n')

def translate_value(i):
    if i >= 32768:
        return f'R{i-32768}'
    else:
        return f'{i:05}'