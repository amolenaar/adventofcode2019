
def parse_memory(line):
    return list(map(int, line.split(",")))

def memory():
    with open("input.txt") as input:
        line = input.readline()

    return parse_memory(line)
139629729
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


def intcode_computer(initial_codes, inputs):
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
            p = inputs.pop()
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


def amplifiers(mem, inputs):
    out = [0]
    for i in inputs:
        out = intcode_computer(list(mem), out + [i])
        assert len(out) == 1
    return out

def gen_inputs(inputs=()):
    if len(inputs) == 5:
        yield inputs
    for i in range(0, 5):
        if i not in inputs:
            yield from gen_inputs(inputs + (i,))

def part1():
    mem = memory()
    out = []
    for inputs in gen_inputs():
        out.append(amplifiers(mem, inputs)[0])
    return max(out)


def gen_inputs2(inputs=()):
    if len(inputs) == 5:
        yield inputs
    for i in range(5, 10):
        if i not in inputs:
            yield from gen_inputs(inputs + (i,))


def part2():
    mem = memory()
    out = []
    for inputs in gen_inputs2():
        out.append(amplifiers(mem, inputs)[0])
    return max(out)


def test_example1():
    mem = parse_memory("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
    assert amplifiers(mem, (4, 3, 2, 1, 0)) == [43210]


def test_example2():
    mem = parse_memory("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
    assert amplifiers(mem, (0, 1, 2, 3, 4)) == [54321]


def test_example3():
    mem = parse_memory("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    assert amplifiers(mem, (1,0,4,3,2)) == [65210]


def test_gen_inputs():
    assert len(list(gen_inputs())) == 120


def test_feedback_example1():
    mem = parse_memory("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
    assert amplifiers(mem, (9,8,7,6,5)) == [139629729]


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
