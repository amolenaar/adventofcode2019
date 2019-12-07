import itertools

def parse_memory(line):
    return list(map(int, line.split(",")))

def memory():
    with open("input.txt") as input:
        line = input.readline()

    return parse_memory(line)


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


def intcode_computer(initial_codes):
    codes = list(initial_codes)
    addr = 0
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
            p = yield
            assert p is not None
            write(codes, i, p, arg1_mode)
            addr += 2
        elif opcode == 4: # output
            _, o = codes[addr:addr+2]
            p = param(codes, o, arg1_mode)
            yield p
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


def amplifiers(mem, inputs):
    out = 0
    for i in inputs:
        c = intcode_computer(list(mem))
        next(c)
        c.send(i)
        out = c.send(out)
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
        out.append(amplifiers(mem, inputs))
    return max(out)


def gen_inputs2(inputs=()):
    if len(inputs) == 5:
        yield inputs
    for i in range(5, 10):
        if i not in inputs:
            yield from gen_inputs2(inputs + (i,))


def amplifiers2(mem, inputs):
    def init(i):
        c = intcode_computer(list(mem))
        next(c) # init
        c.send(i) # read first input
        return c

    amps = [init(i) for i in inputs]

    signal = 0
    output = 0
    for amp in itertools.cycle(amps):
        try:
            out = amp.send(signal)
        except StopIteration:
            return output
        if out is not None:
            signal = out
            if amp is amps[-1]:
                output = signal
            continue # allow to send signal into next amp


def part2():
    mem = memory()
    out = []
    for inputs in gen_inputs2():
        out.append(amplifiers2(mem, inputs))
    return max(out)


def test_example1():
    mem = parse_memory("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
    assert amplifiers(mem, (4, 3, 2, 1, 0)) == 43210


def test_example2():
    mem = parse_memory("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
    assert amplifiers(mem, (0, 1, 2, 3, 4)) == 54321


def test_example3():
    mem = parse_memory("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    assert amplifiers(mem, (1,0,4,3,2)) == 65210


def test_gen_inputs():
    assert len(list(gen_inputs())) == 120


def test_feedback_example1():
    mem = parse_memory("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
    assert amplifiers2(mem, (9,8,7,6,5)) == 139629729


def test_feedback_example2():
    mem = parse_memory("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")
    assert amplifiers2(mem, (9,7,8,5,6)) == 18216


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
