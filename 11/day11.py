import itertools

def parse_memory(line):
    return list(map(int, line.split(",")))

def memory():
    with open("input.txt") as input:
        line = input.readline()

    return parse_memory(line)


def read(codes, addr, offset):
    return tuple(codes[a] for a in range(addr, addr+offset))

def param(codes, index_or_val, mode, relative_base):
    if mode == 1:
        return index_or_val
    elif mode == 2:
        return codes.get(relative_base + index_or_val, 0)
    elif mode == 0:
        return codes.get(index_or_val, 0)
    else:
        raise ValueError(f"Invalid mode {mode}")


def write(codes, index, val, mode, relative_base):
    if mode == 0:
        codes[index] = val
    elif mode == 2:
        codes[relative_base + index] = val
    else:
        raise ValueError(f"Invalid mode {mode}")


def intcode_computer(initial_codes):
    codes = dict(enumerate(initial_codes))
    addr = 0
    relative_base = 0
    inputs = []
    heap = {}
    while True:
        instr = codes[addr]
        arg3_mode = instr // 10000
        arg2_mode = (instr // 1000) % 10
        arg1_mode = (instr // 100) % 10
        opcode = instr % 100

        if opcode == 99: # exit
            break
        elif opcode == 1: # add
            _, i1, i2, o = read(codes, addr, 4)
            p1 = param(codes, i1, arg1_mode, relative_base)
            p2 = param(codes, i2, arg2_mode, relative_base)
            write(codes, o, p1 + p2, arg3_mode, relative_base)
            addr += 4
        elif opcode == 2: # multiply
            _, i1, i2, o = read(codes, addr, 4)
            p1 = param(codes, i1, arg1_mode, relative_base)
            p2 = param(codes, i2, arg2_mode, relative_base)
            write(codes, o, p1 * p2, arg3_mode, relative_base)
            addr += 4
        elif opcode == 3: # input
            _, i = read(codes, addr, 2)
            if inputs:
                p = inputs.pop()
            else:
                p = yield
            assert p is not None
            write(codes, i, p, arg1_mode, relative_base)
            addr += 2
        elif opcode == 4: # output
            _, o = read(codes, addr, 2)
            p = param(codes, o, arg1_mode, relative_base)
            inp = yield p
            if inp is not None:
                inputs.append(inp)
            addr += 2
        elif opcode == 5: # jump-if-true
            _, i, o = read(codes, addr, 3)
            p = param(codes, i, arg1_mode, relative_base)
            ip = param(codes, o, arg2_mode, relative_base)
            if p:
                addr = ip
            else:
                addr += 3
        elif opcode == 6: # jump-if-false
            _, i, o = read(codes, addr, 3)
            p = param(codes, i, arg1_mode, relative_base)
            ip = param(codes, o, arg2_mode, relative_base)
            if not p:
                addr = ip
            else:
                addr += 3
        elif opcode == 7: # less-than
            _, i1, i2, o = read(codes, addr, 4)
            p1 = param(codes, i1, arg1_mode, relative_base)
            p2 = param(codes, i2, arg2_mode, relative_base)
            write(codes, o, int(p1 < p2), arg3_mode, relative_base)
            addr += 4
        elif opcode == 8: # equal-to
            _, i1, i2, o = read(codes, addr, 4)
            p1 = param(codes, i1, arg1_mode, relative_base)
            p2 = param(codes, i2, arg2_mode, relative_base)
            write(codes, o, int(p1 == p2), arg3_mode, relative_base)
            addr += 4
        elif opcode == 9: # relative-base
            _, i = read(codes, addr, 2)
            relative_base += param(codes, i, arg1_mode, relative_base)
            addr += 2
        else:
            raise ValueError(f"Invalid code {opcode} at addr {addr}")


DIR_UP = (0, -1)
DIR_RIGHT = (1, 0)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)

TURN_LEFT = 0
TURN_RIGHT = 1

def change_direction(direction, turn):
    if turn == TURN_LEFT: # left 90 deg
        go_left = [DIR_UP, DIR_LEFT, DIR_DOWN, DIR_RIGHT, DIR_UP]
        return go_left[go_left.index(direction) + 1]
    elif turn == TURN_RIGHT: # right 90 deg
        go_right = [DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP]
        return go_right[go_right.index(direction) + 1]


def robot(mem, start_panel=0):
    panels = {}
    pos = (0, 0)
    direction = DIR_UP
    c = intcode_computer(list(mem))
    next(c)
    try:
        while True:
            color = c.send(panels.get(pos, start_panel))
            start_panel = 0
            turn = next(c)
            panels[pos] = color
            direction = change_direction(direction, turn)
            pos = (pos[0] + direction[0], pos[1] + direction[1])
    except StopIteration:
        return panels


def test_directions():
    assert change_direction((0, -1), TURN_LEFT) == (-1, 0)
    assert change_direction((0, -1), TURN_RIGHT) == (1, 0)

def part1():
    panels = robot(memory())
    paint(panels)
    return len(panels)

def paint(panels):
    white = {k: v for k, v in panels.items() if v == 1}
    xs = [x for x, y in white]
    ys = [y for x, y in white]
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            print("#" if (x, y) in white else " ", end='')
        print("")

def part2():
    panels = robot(memory(), 1)
    paint(panels)
    return "LPZKLGHR"


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
