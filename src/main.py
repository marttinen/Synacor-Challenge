from vm import VirtualMachine

if __name__ == '__main__':
    with open('challenge.bin', 'rb') as f:
        program = bytearray(f.read())
    vm = VirtualMachine(program)
    vm.start()
    print('vm done.')
