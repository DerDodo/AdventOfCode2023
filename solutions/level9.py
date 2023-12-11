from typing import Tuple

from util.file_util import read_input_file


def level9() -> Tuple[int, int]:
    lines = parse_input_file()
    extrapolations = list(map(extrapolate, lines))
    return sum(map(lambda tuples: tuples[0], extrapolations)), sum(map(lambda tuples: tuples[1], extrapolations))


def parse_input_file() -> list[list[int]]:
    lines = read_input_file(9)
    lines = map(lambda line: list(map(int, line.split(" "))), lines)
    return list(lines)


def extrapolate(values: list[int]) -> Tuple[int, int]:
    differences = list()
    differences.append(values)
    while differences[-1].count(0) != len(differences[-1]):
        check_line = differences[-1]
        next_difference = [check_line[idx + 1] - number for idx, number in enumerate(check_line[0:-1])]
        differences.append(next_difference)
    future = sum(map(lambda line: line[-1], differences))
    past = sum([(num if idx % 2 == 0 else -num) for idx, num in enumerate(map(lambda line: line[0], differences))])
    return future, past


if __name__ == '__main__':
    print("Sum values: " + str(level9()))


def test_level9():
    assert (114, 2) == level9()
