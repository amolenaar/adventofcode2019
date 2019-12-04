from itertools import groupby, tee

input = (147981, 691423)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def matches(n):
    adjecent = False
    for a, b in pairwise(str(n)):
        if a > b:
            return False
        if a == b:
            adjecent = True
    return adjecent


def all_matches(a, b, matcher=matches):
    for n in range(a, b):
        if matcher(n):
            yield n


def part1():
    m = all_matches(*input)

    return len(list(m))


def better_matches(n):
    for a, b in pairwise(str(n)):
        if a > b:
            return False
    return bool([True for k, g in groupby(str(n)) if len(list(g)) == 2])


def part2():
    m = all_matches(*input, matcher=better_matches)

    return len(list(m))

def test_match():
    assert matches(111111)
    assert not matches(223450)
    assert not matches(123789)


def test_better_matches():
    assert better_matches(112233)
    assert not better_matches(123444)
    assert better_matches(111122)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
