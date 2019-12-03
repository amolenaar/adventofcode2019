
def split_line(line):
    return map(lambda s: (s[0], int(s[1:])), line.split(","))


def path_to_segments(path):
    pos = (0, 0)
    for (dir, dist) in path:
        curpos = pos
        if dir == "U":
            pos = (pos[0], pos[1] + dist)
        elif dir == "D":
            pos = (pos[0], pos[1] - dist)
        elif dir == "R":
            pos = (pos[0] + dist, pos[1])
        elif dir == "L":
            pos = (pos[0] - dist, pos[1])
        yield (curpos, pos)


def steps(seg):
    return abs(seg[0][0] - seg[1][0]) + abs(seg[0][1] - seg[1][1])


def crossing(seg1, seg2):
    p11, p12 = seg1
    p21, p22 = seg2
    # Parallel
    if (p11[0] == p12[0] and p21[0] == p22[0]) or (p11[1] == p12[1] and p21[1] == p22[1]):
        return False
    if (p21[0] <= p11[0] <= p22[0] or p22[0] <= p11[0] <= p21[0]) and \
       (p11[1] <= p21[1] <= p12[1] or p12[1] <= p21[1] <= p11[1]):
        c = (p11[0], p21[1])
        return c, steps((p11, c)) + steps((p21, c))
    if (p21[1] <= p11[1] <= p22[1] or p22[1] <= p11[1] <= p21[1]) and \
       (p11[0] <= p21[0] <= p12[0] or p12[0] <= p21[0] <= p11[0]):
        c = (p21[0], p11[1])
        return c, steps((p11, c)) + steps((p21, c))
    return 


def find_crossings(wire1, wire2):
    for seg1 in wire1:
        for seg2 in wire2:
            c = crossing(seg1, seg2)
            if c:
                yield c[0]

def part1():
    with open("input.txt") as f:
        lines = f.readlines()

    wire1 = path_to_segments(split_line(lines[0]))
    wire2 = path_to_segments(split_line(lines[1]))


    crossings = find_crossings(wire1, wire2)
    return min(crossings, key=lambda c: c[0] + c[1])


def find_steps(wire1, wire2):
    wire2 = list(wire2)
    steps1 = 0
    for seg1 in wire1:
        steps2 = 0
        for seg2 in wire2:
            c = crossing(seg1, seg2)
            if c and c[0] != (0, 0):
                yield c[1] + steps1 + steps2
            steps2 += steps(seg2)
        steps1 += steps(seg1)


def part2():
    with open("input.txt") as f:
        lines = f.readlines()

    wire1 = path_to_segments(split_line(lines[0]))
    wire2 = path_to_segments(split_line(lines[1]))


    steps = find_steps(wire1, wire2)
    return min(steps)


def test_split_line():
    assert list(split_line("R12,U78")) == [("R", 12), ("U", 78)]


def test_path_to_segments():
    assert list(path_to_segments([("R", 12), ("U", 78)])) == [((0, 0), (12, 0)), ((12, 0), (12, 78))]


def test_crossing():
    assert crossing(((4, 1), (4, -1)), ((0, 0), (10, 0))) == ((4, 0), 4 + 1)
    assert crossing(((0, 0), (10, 0)), ((4, 11), (4, -1))) == ((4, 0), 4 + 11)


def test_no_crossing():
    assert crossing(((0, 0), (10, 0)), ((4, 1), (4, 3))) == None
    assert crossing(((0, 0), (-10, 0)), ((4, 1), (4, -1))) == None


def test_part_example_input():
    wire1 = path_to_segments(split_line("R8,U5,L5,D3"))
    wire2 = path_to_segments(split_line("U7,R6,D4,L4"))

    steps = find_steps(wire1, wire2)
    assert min(steps) == 30


def test_first_example_input():
    wire1 = path_to_segments(split_line("R75,D30,R83,U83,L12,D49,R71,U7,L72"))
    wire2 = path_to_segments(split_line("U62,R66,U55,R34,D71,R55,D58,R83"))

    steps = find_steps(wire1, wire2)
    assert min(steps) == 610


def test_second_example_input():
    wire1 = path_to_segments(split_line("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"))
    wire2 = path_to_segments(split_line("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))

    steps = find_steps(wire1, wire2)
    assert min(steps) == 410


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
