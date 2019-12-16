from itertools import cycle

BASE_PATTERN = [0, 1, 0, -1]


def read_input():
    with open("input.txt") as f:
        return map(int, f.readline().strip())


def read_input2():
    with open("input.txt") as f:
        return map(int, f.readline().strip() * 10000)

def pattern(iteration):
    start = True
    for n in cycle(BASE_PATTERN):
        for _ in range(iteration+1):
            if start:
                start = False
            else:
                yield n

def phase(input_list):
    for i, _ in enumerate(input_list):
        yield abs(sum(m*n for n, m in zip(input_list, pattern(i)))) % 10


def test_phase():
    input_list = list(map(int, "12345678"))
    phase1_list = list(phase(input_list))
    assert phase1_list == [4,8,2,2,6,1,5,8]
    phase2_list = list(phase(phase1_list))
    assert phase2_list == [3,4,0,4,0,4,3,8]


def as_int(input_list):
    return int("".join(map(str, input_list)))


def test_part1():
    input_list = list(read_input())

    for _ in range(100):
        input_list = list(phase(input_list))

    assert as_int(input_list[:8]) == 32002835
    

def test_part2():
    input_list = list(read_input())
    offset = as_int(input_list[:7])
    input_list = input_list * 10000
    assert offset > len(input_list) / 2
    # everything before offset is multiplied by 0, so we can skip that
    input_list = input_list[offset:]

    # Offset is past the halfway point of the list: so all multipliers are 1
    for _ in range(100):
        for i in range(len(input_list)-1, 0, -1):
            input_list[i-1] = (input_list[i-1] + input_list[i]) % 10

    assert as_int(input_list[:8]) == 69732268


