
def count_orbits(orbit_map, obj):
    if obj == "COM":
        return 0
    orbits = orbit_map[obj]
    return 1 + count_orbits(orbit_map, orbits)


def path(orbit_map, obj):
    if obj == "COM":
        return []
    orbits = orbit_map[obj]
    return [orbits] + path(orbit_map, orbits)

def count_all_orbits(orbit_map):
    return sum([count_orbits(orbit_map, obj) for obj in orbit_map])


def test_small_orbits():
    orbit_map = {b: a for a, b in map(lambda s: s.split(")"), [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        ])}
    assert count_orbits(orbit_map, "D") == 3
    assert count_orbits(orbit_map, "L") == 7
    assert count_all_orbits(orbit_map) == 42

def test_small_path():
    orbit_map = {b: a for a, b in map(lambda s: s.split(")"), [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN",
        ])}
    you = path(orbit_map, "YOU")
    san = path(orbit_map, "SAN")

    assert "D" in you
    assert "D" in san
    assert set(you) - set(san) == set(["E", "J", "K"])
    assert set(san) - set(you) == set(["I"])


def read_input():
    with open("input.txt") as f:
        lines = f.readlines()

    orbit_map = dict({b: a for a, b in map(lambda s: s.strip().split(')'), lines)})
    return orbit_map


def part1():
    orbit_map = read_input()

    assert len(orbit_map) == 1868

    return count_all_orbits(orbit_map)


def part2():
    orbit_map = read_input()

    you = path(orbit_map, "YOU")
    san = path(orbit_map, "SAN")
    you_to_common = set(you) - set(san)
    san_to_common = set(san) - set(you)
    return len(you_to_common) + len(san_to_common)


if __name__ == '__main__':
    print("Part 1:", part1())
    print("Part 2:", part2())
