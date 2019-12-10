
from itertools import groupby
import math


def data():
    with open("input.txt") as f:
        return list(map(str.strip, f.readlines()))


def degrees(origin, pos):
    return (360 + 90 + math.degrees(math.atan2(pos[1]-origin[1], pos[0]-origin[0]))) % 360


def as_coords(data):
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "#":
                yield (x, y)


def part1():
    coords = list(as_coords(data()))

    all_coords = {o: set([degrees(o, p) for p in coords]) for o in coords}

    return max(len(v) for v in all_coords.values())


def part2():
    coords = list(as_coords(data()))

    all_coords = {o: [(degrees(o, p), p) for p in coords] for o in coords}

    _, group = max((len(set(a for a, b in v)), sorted(v)) for v in all_coords.values())

    group = [(k, [b for _, b in v]) for k, v in groupby(group, key=lambda d: d[0])]
    return group[200 - 1]


def test_data():
    d = data()
    assert d[0] == "#.#....#.#......#.....#......####."


def test_as_coords():
    data = ["#..#", ".#.."]

    assert list(as_coords(data)) == [(0, 0), (3, 0), (1, 1)]


def test_degrees():
    assert degrees((0, 0), (0, -2)) == 0
    assert degrees((0, 0), (-2, 0)) == 270
    assert degrees((0, 0), (2, 0)) == 90
    assert degrees((0, 0), (-2, -2)) == 315


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
