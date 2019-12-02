
with open("input.txt") as input:
    line = input.readline()

memory = list(map(int, line.split(",")))

def intcode_computer(initial_codes):
    codes = list(initial_codes)
    addr = 0
    while True:
        opcode, i1, i2, o = codes[addr:addr+4]
        if opcode == 99:
            break
        elif opcode == 1: 
            codes[o] = codes[i1] + codes[i2]
        elif opcode == 2: 
            codes[o] = codes[i1] * codes[i2]
        else:
            raise f"Invalid code {opcode} at addr {addr}"
        addr += 4
    return codes[0]


memory[1] = 12
memory[2] = 2
print(f"Day 2, part 1: {intcode_computer(memory)}")


mb = list(memory)
for noun in range(0, 100):
    for verb in range(0, 100):
        memory[1] = noun
        memory[2] = verb
        output = intcode_computer(memory)
        if output == 19690720:
            print(f"Day 2, part 2: {100 * noun + verb}")
            break;

