
import math

with open("input.txt") as input:
    lines = input.readlines()

masses = list(map(int, lines))

fuel_req = map(lambda m: math.floor(m/3)-2, masses)

print("part 1", sum(fuel_req))

def calc_fuel2(m):
    f = math.floor(m/3)-2
    if f <= 0:
        return 0
    else:
        return f + calc_fuel2(f)

fuel_req2 = map(calc_fuel2, masses)

print("part 2", sum(fuel_req2))
