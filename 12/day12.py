
from itertools import permutations, count
from pprint import pprint

class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0
    
    def __str__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.vx}, y={self.vy}, z={self.vz}>"

    __repr__ = __str__

    def t(self):
        return (self.x, self.y, self.z, self.vx, self.vy, self.vz)


def cmp(a, b):
    if a > b:
        return -1
    elif a < b:
        return 1
    return 0


def gravity(ma, mb):
    ma.vx += cmp(ma.x, mb.x)
    ma.vy += cmp(ma.y, mb.y)
    ma.vz += cmp(ma.z, mb.z)


def position(m):
    m.x += m.vx
    m.y += m.vy
    m.z += m.vz


def time_step(moons):
    for ma, mb in permutations(moons, 2):
        gravity(ma, mb)
    for m in moons:
        position(m)


def total_energy(m):
    return (abs(m.x) + abs(m.y) + abs(m.z)) * (abs(m.vx) + abs(m.vy) + abs(m.vz))


def part1():
    moons = [
        Moon(x=15, y=-2, z=-6),
        Moon(x=-5, y=-4, z=-11),
        Moon(x=0, y=-6, z=0),
        Moon(x=5, y=9, z=6)
    ]
    for x in range(1000):
        time_step(moons)

    return sum(total_energy(m) for m in moons)


def one_round(moons):
    initial = [m.t() for m in moons]
    periods = [None for m in moons]

    time_step(moons)
    for time in count(1):
        #if time % 1000 == 0:
        #    print("time:", time)
        for i, m in enumerate(moons):
            if m.t() == initial[i] and not periods[i]:
                print("Periods", i, time)
                periods[i] = time
        if all(periods):
            break
        time_step(moons)

    return periods


def part2():
    moons = [
        Moon(x=15, y=-2, z=-6),
        Moon(x=-5, y=-4, z=-11),
        Moon(x=0, y=-6, z=0),
        Moon(x=5, y=9, z=6)
    ]
    return one_round(moons)

def test_gravity():
    ma = Moon(x=15, y=-2, z=-6)
    mb = Moon(x=-5, y=-4, z=-11)

    gravity(ma, mb)
    
    assert ma.vx == -1
    assert ma.vy == -1
    assert ma.vz == -1


def test_time_step_gravity():
    moons = [
        Moon(x=-1, y=0, z=2),
        Moon(x=2, y=-10, z=-7),
        Moon(x=4, y=-8, z=8),
        Moon(x=3, y=5, z=-1)
    ]
    pprint(moons)
    time_step(moons)
    pprint(moons)
    assert moons[0].x == 2
    assert moons[0].y == -1
    assert moons[0].z == 1


def test_previous_state():
    moons = [
        Moon(x=-1, y=0, z=2),
        Moon(x=2, y=-10, z=-7),
        Moon(x=4, y=-8, z=8),
        Moon(x=3, y=5, z=-1)
    ]
    periods = one_round(moons)

    print( 924*924*2772*2772 )
    assert periods == []

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())


