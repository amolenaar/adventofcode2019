
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def data():
    with open("input.txt") as f:
        return f.readline().strip()


def count(l, m):
    return sum(1 for v in l if v == m)


def test_grouper():
    gr = grouper("abcdefghijklmnopqr", 6)
    assert "".join(next(gr)) == "abcdef"
    assert "".join(next(gr)) == "ghijkl"
    assert "".join(next(gr)) == "mnopqr"


def test_layers():
    assert len(data()) / (25*6) == 100


def test_count_zeros():
    assert count_zeros("1203405607") == 3


def part1():
    layer = min((count(layer, "0"), layer) for layer in grouper(data(), 25*6))[1]
    return count(layer, "1") * count(layer, "2")


if __name__ == "__main__":
    print("Part 1:", part1())

