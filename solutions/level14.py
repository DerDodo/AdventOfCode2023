import math

from util.file_util import read_input_file


def level14_1() -> int:
    field = parse_input_file()
    tilt_north(field)
    return get_total_weight(field)


def level14_2() -> int:
    field = parse_input_file()
    weights = []
    num_repetitions = 500

    for _ in range(0, num_repetitions):
        tilt_north(field)
        tilt_west(field)
        tilt_south(field)
        tilt_east(field)
        weights.append(get_total_weight(field))

    return get_weight_by_extrapolate_patterns(weights, 1000000000)


def parse_input_file() -> list[list[str]]:
    lines = read_input_file(14)
    return list(map(list, lines))


def find_stones(field: list[list[str]]) -> list[tuple[int, int]]:
    stones = []
    for y in range(0, len(field)):
        for x in range(0, len(field[0])):
            if field[y][x] == "O":
                stones.append((x, y))
    return stones


def tilt_north(field: list[list[str]]):
    for y in range(0, len(field)):
        for x in range(0, len(field[0])):
            if field[y][x] == "O":
                move_to = y
                while move_to > 0 and field[move_to - 1][x] == ".":
                    move_to -= 1
                field[y][x] = "."
                field[move_to][x] = "O"


def tilt_south(field: list[list[str]]):
    for y in reversed(range(0, len(field) - 1)):
        for x in range(0, len(field[0])):
            if field[y][x] == "O":
                move_to = y
                while move_to < len(field) - 1 and field[move_to + 1][x] == ".":
                    move_to += 1
                field[y][x] = "."
                field[move_to][x] = "O"


def tilt_west(field: list[list[str]]):
    for x in range(0, len(field[0])):
        for y in range(0, len(field)):
            if field[y][x] == "O":
                move_to = x
                while move_to > 0 and field[y][move_to - 1] == ".":
                    move_to -= 1
                field[y][x] = "."
                field[y][move_to] = "O"


def tilt_east(field: list[list[str]]):
    for x in reversed(range(0, len(field[0]))):
        for y in range(0, len(field)):
            if field[y][x] == "O":
                move_to = x
                while move_to < len(field) - 1 and field[y][move_to + 1] == ".":
                    move_to += 1
                field[y][x] = "."
                field[y][move_to] = "O"


def get_total_weight(field: list[list[str]]) -> int:
    height = len(field)
    total_sum = 0
    for i, line in enumerate(field):
        total_sum += line.count("O") * (height - i)
    return total_sum


def get_weight_by_extrapolate_patterns(weights: list[int], total_cycles: int) -> int:
    pattern_length = find_pattern_length(weights)
    how_many_more_patterns = math.ceil((total_cycles - len(weights)) / pattern_length)
    pattern_end_after_filling_up = len(weights) + pattern_length * how_many_more_patterns
    overshoot = pattern_end_after_filling_up - total_cycles
    return weights[-1-overshoot]


def find_pattern_length(weights: list[int]) -> int:
    min_pattern_length = 10
    for check_back_i in range(min_pattern_length, len(weights) - 1):
        pattern_length = check_back_i + 1
        if is_pattern(weights, pattern_length):
            return pattern_length
    return -1


def is_pattern(weights: list[int], pattern_length: int) -> int:
    num_to_find = weights[-1]
    if weights[-1 - pattern_length] == num_to_find and weights[-1 - pattern_length * 2] == num_to_find:
        for pattern_i in range(1, pattern_length):
            pattern_num = weights[-1-pattern_i]
            if (weights[-1 - pattern_length - pattern_i] != pattern_num and
                    weights[-1 - pattern_length * 2 - pattern_i] != pattern_num):
                return False
        return True
    return False


if __name__ == '__main__':
    print("Weight only north: " + str(level14_1()))
    print("Weight cycle: " + str(level14_2()))


def test_level13():
    assert 136 == level14_1()
    assert 64 == level14_2()
