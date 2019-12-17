import itertools
import time

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
            assert inputs == []
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
                p = yield "!"
            assert p is not None
            write(codes, i, p, arg1_mode, relative_base)
            addr += 2
        elif opcode == 4: # output
            _, o = read(codes, addr, 2)
            p = param(codes, o, arg1_mode, relative_base)
            inp = yield p
            if inp is not None:
                inputs.insert(0, inp)
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

DIRS = [0, DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT]

TURN_LEFT = 0
TURN_RIGHT = 1

def change_direction(direction, turn):
    if turn == TURN_LEFT: # left 90 deg
        go_left = [DIR_UP, DIR_LEFT, DIR_DOWN, DIR_RIGHT, DIR_UP]
        return go_left[go_left.index(direction) + 1]
    elif turn == TURN_RIGHT: # right 90 deg
        go_right = [DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP]
        return go_right[go_right.index(direction) + 1]


def paint(panels):
    tiles = [' ', '\033[35m#', '\033[32m%', '\033[33;1m-\033[0m', '\033[31mo']
    xs, ys = zip(*panels.keys())
    print(f"\033[{max(ys)-min(ys)+1}A")
    for y in range(min(ys), max(ys) + 1):
        print("    ", end="")
        for x in range(min(xs), max(xs) + 1):
            print(tiles[panels.get((x, y), 0)], end="")
        print("\033[0m")


def ascii(mem):
    x = y = 0
    grid = {}
    c = intcode_computer(list(mem))
    try:
        while True:
            v = next(c)
            print(chr(v), end="")
            if v == 35:
                grid[x, y] = 35
            if v == 10:
                x = 0
                y += 1
            else:
                x += 1

    except StopIteration:
        return grid


def find_intersections(grid):
    for x, y in grid:
        if (x+1, y) in grid and (x-1, y) in grid and (x, y-1) in grid and (x, y+1) in grid:
            yield (x, y)


def part1():
    grid = ascii(memory())
    isects = find_intersections(set(grid.keys()))
    return sum(x*y for x, y in isects)


def vacuum(mem, prog):
    c = intcode_computer(list(mem))
    next(c)
    for a in prog:
        c.send(ord(a))
    try:
        while True:
            v = next(c)
    except StopIteration:
        return v


def part2():
    #   A   R,4,L,10,L,10
    #   B   L,8,R,12,R,10,R,4
    #   A   R,4,L,10,L,10
    #   B   L,8,R,12,R,10,R,4
    #   A   R,4,L,10,L,10
    #   C   L,8,L,8,R,10,R,4
    #   B   L,8,R,12,R,10,R,4
    #   C   L,8,L,8,R,10,R,4
    #   A   R,4,L,10,L,10
    #   C   L,8,L,8,R,10,R,4
    main_routine = "A,B,A,B,A,C,B,C,A,C\n"
    function_a = "R,4,L,10,L,10\n"
    function_b = "L,8,R,12,R,10,R,4\n"
    function_c = "L,8,L,8,R,10,R,4\n"
    video_feed = "n\n"

    mem = memory()
    mem[0] = 2

    out = vacuum(mem, main_routine+function_a+function_b+function_c+video_feed)
    return out


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
