from functools import reduce
from operator import mul

def parse_input_lines(lines):
    for line in lines:
        inputs, output = line.split("=>")
        inputs = [(int(q), m) for q, m in [s.split() for s in map(str.strip, inputs.split(","))]]
        output = [(int(q), m) for q, m in [output.strip().split()]][0]
        yield tuple(inputs), output


def read_input():
    with open("input.txt") as f:
        return f.readlines()


def map_reactions(raw_reactions):
    return {v: (q, k) for k, (q, v) in raw_reactions}


def reduce_to_ore(input, reactions, mult=1):
    print('reduce', input)
    q, p = input
    if p == "ORE":
        yield mult/q
    else:
        mult = mult * q
        divider, reacts = reactions.get(p)
        for r in reacts:
            yield from reduce_to_ore(r, reactions, mult * divider)


FUEL = "FUEL"


def part1():
    reactions = {v: k for k, v in parse_input_lines(read_input())}
    ore = reduce_to_ore([1, FUEL], reactions)
    return reactions


def test_input():
    assert next(parse_input_lines(["2 MPHSH, 3 NQNX => 3 FWHL"])) == (((2, "MPHSH"), (3, "NQNX")), (3, "FWHL"))


def test_map_reactions():
    assert map_reactions([(((2, "MPHSH"), (3, "NQNX")), (3, "FWHL"))]) == {'FWHL': (3, ((2, 'MPHSH'), (3, 'NQNX')))}

def test_reduce_to_ore():
    reactions = [
        "10 ORE => 10 A",
        "1 ORE => 1 B",
        "7 A, 1 B => 1 C",
        "7 A, 1 C => 1 D",
        "7 A, 1 D => 1 E",
        "7 A, 1 E => 1 FUEL"]
    reactions = map_reactions(parse_input_lines(reactions))
    ore = list(reduce_to_ore((1, FUEL), reactions))

    #assert sum(mul, ore) == 175
    assert ore == ""


if __name__ == "__main__":
    print("Part 1", part1())
