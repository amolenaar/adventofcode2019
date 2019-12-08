
from itertools import dropwhile, zip_longest


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


def align_pixels(layers):
    return zip(*layers)


def find_color(pixels):
    return next(dropwhile(lambda p: p == "2", pixels))


def test_grouper():
    gr = grouper("abcdefghijklmnopqr", 6)
    assert "".join(next(gr)) == "abcdef"
    assert "".join(next(gr)) == "ghijkl"
    assert "".join(next(gr)) == "mnopqr"


def test_layers():
    assert len(data()) / (25*6) == 100


def test_count_zeros():
    assert count("1203405607", "0") == 3


def test_align_pixels():
    data = "0222112222120000"
    pixels = align_pixels(grouper(data, 4))
    assert next(pixels) == ("0", "1", "2", "0")
    assert next(pixels) == ("2", "1", "2", "0")

    
def test_find_color():
    assert find_color(("0", "1", "2", "0")) == "0"
    assert find_color(("2", "2", "2", "1")) == "1"


def part1():
    layer = min((count(layer, "0"), layer) for layer in grouper(data(), 25*6))[1]
    return count(layer, "1") * count(layer, "2")


def part2():
    image = map(find_color, align_pixels(grouper(data(), 25*6)))
    for line in grouper(image, 25):
        print("".join(line).replace("0", " "))


if __name__ == "__main__":
    print("Part 1:", part1())
    part2()
    print("Part 2: PHPEU")

