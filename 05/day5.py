
with open("input.txt") as input:
    line = input.readline()

memory = list(map(int, line.split(",")))

def param(codes, index_or_val, mode):
    if mode == 1:
        return index_or_val
    elif mode == 0:
        return codes[index_or_val]
    else:
        raise ValueError(f"Invalid mode {mode}")


def write(codes, index_or_val, val, mode):
    if mode == 0:
        codes[index_or_val] = val
    else:
        raise ValueError(f"Invalid mode {mode}")


def intcode_computer(initial_codes, inputs=[]):
    codes = list(initial_codes)
    addr = 0
    outputs = []
    while True:
        instr = codes[addr]
        arg3_mode = instr // 10000
        arg2_mode = (instr // 1000) % 10
        arg1_mode = (instr // 100) % 10
        opcode = instr % 100

        if opcode == 99:
            break
        elif opcode == 1: 
            _, i1, i2, o = codes[addr:addr+4]
            p1 = param(codes, i1, arg1_mode)
            p2 = param(codes, i2, arg2_mode)
            write(codes, o, p1 + p2, arg3_mode)
            addr += 4
        elif opcode == 2: 
            _, i1, i2, o = codes[addr:addr+4]
            p1 = param(codes, i1, arg1_mode)
            p2 = param(codes, i2, arg2_mode)
            write(codes, o, p1 * p2, arg3_mode)
            addr += 4
        elif opcode == 3: 
            _, i = codes[addr:addr+2]
            p = inputs[0]
            write(codes, i, p, arg1_mode)
            addr += 2
        elif opcode == 4: 
            _, o = codes[addr:addr+2]
            p = param(codes, o, arg1_mode)
            outputs.append(p)
            addr += 2
        else:
            raise ValueError(f"Invalid code {opcode} at addr {addr}")
    return outputs


def intcode_computer2(initial_codes, inputs=[]):
    codes = list(initial_codes)
    addr = 0
    outputs = []
    while True:
        instr = codes[addr]
        arg3_mode = instr // 10000
        arg2_mode = (instr // 1000) % 10
        arg1_mode = (instr // 100) % 10
        opcode = instr % 100

        if opcode == 99: # exit
            break
        elif opcode == 1: # add
            _, i1, i2, o = codes[addr:addr+4]
            p1 = param(codes, i1, arg1_mode)
            p2 = param(codes, i2, arg2_mode)
            write(codes, o, p1 + p2, arg3_mode)
            addr += 4
        elif opcode == 2: # multiply
            _, i1, i2, o = codes[addr:addr+4]
            p1 = param(codes, i1, arg1_mode)
            p2 = param(codes, i2, arg2_mode)
            write(codes, o, p1 * p2, arg3_mode)
            addr += 4
        elif opcode == 3: # input
            _, i = codes[addr:addr+2]
            p = inputs[0]
            write(codes, i, p, arg1_mode)
            addr += 2
        elif opcode == 4: # output
            _, o = codes[addr:addr+2]
            p = param(codes, o, arg1_mode)
            outputs.append(p)
            addr += 2
        elif opcode == 5: # jump-if-true
            _, i, o = codes[addr:addr+3]
            p = param(codes, i, arg1_mode)
            ip = param(codes, o, arg2_mode)
            if p:
                addr = ip
            else:
                addr += 3
        elif opcode == 6: # jump-if-false
            _, i, o = codes[addr:addr+3]
            p = param(codes, i, arg1_mode)
            ip = param(codes, o, arg2_mode)
            if not p:
                addr = ip
            else:
                addr += 3
        elif opcode == 7: # less-than
            _, i1, i2, o = codes[addr:addr+4]
            p1 = param(codes, i1, arg1_mode)
            p2 = param(codes, i2, arg2_mode)
            write(codes, o, int(p1 < p2), arg3_mode)
            addr += 4
        elif opcode == 8: # equal-to
            _, i1, i2, o = codes[addr:addr+4]
            p1 = param(codes, i1, arg1_mode)
            p2 = param(codes, i2, arg2_mode)
            write(codes, o, int(p1 == p2), arg3_mode)
            addr += 4
        else:
            raise ValueError(f"Invalid code {opcode} at addr {addr}")
    return outputs


def part1():
    output = intcode_computer(memory, [1])
    return output[-1]


def part2():
    output = intcode_computer2(memory, [5])
    return output


def test_param():
    assert param([11,22,33,44,55], 3, 0) == 44
    assert param([11,22,33,44,55], 3, 1) == 3


def test_part1():
    assert intcode_computer(memory, [1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 7286649]


def test_part_2_computer_example_1():
    line = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    instr = list(map(int, line.split(",")))
    assert intcode_computer2(instr, [0]) == [0]
    assert intcode_computer2(instr, [1]) == [1]


def test_part_2_computer_example_2():
    line = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
    instr = list(map(int, line.split(",")))
    assert intcode_computer2(instr, [0]) == [0]
    assert intcode_computer2(instr, [1]) == [1]


def test_part_2_computer_example_3():
    line = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    instr = list(map(int, line.split(",")))
    assert intcode_computer2(instr, [5]) == [999]
    assert intcode_computer2(instr, [7]) == [999]
    assert intcode_computer2(instr, [8]) == [1000]
    assert intcode_computer2(instr, [9]) == [1001]
    assert intcode_computer2(instr, [11]) == [1001]


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
