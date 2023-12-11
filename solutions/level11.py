from util.file_util import read_input_file
from util.math_util import transpose


def find_empty_lines(field: list[list[str]]) -> list[int]:
    return list(
        map(lambda result: result[0],
            filter(lambda line: line[1].count(".") == len(line[1]),
                   enumerate(field))))


class Universe:
    field: list[list[str]]
    galaxies: list[tuple[int, int]]
    empty_lines: list[int]
    empty_cols: list[int]

    def __init__(self, field: list[str]):
        self.field = list(map(list, field))
        self.empty_lines = find_empty_lines(self.field)
        self.empty_cols = find_empty_lines(transpose(self.field))
        self.galaxies = self.__find_galaxies()

    def __find_galaxies(self) -> list[tuple[int, int]]:
        galaxies = []
        for y, line in enumerate(self.field):
            for x, char in enumerate(line):
                if char == "#":
                    galaxies.append((x, y))
        return galaxies

    def get_distance(self, galaxy1: tuple[int, int], galaxy2: tuple[int, int], expand_by: int) -> int:
        sum_distances = 0
        sum_distances += abs(galaxy1[0] - galaxy2[0])
        sum_distances += abs(galaxy1[1] - galaxy2[1])
        sum_distances += sum(
            min(galaxy1[1], galaxy2[1]) < line < max(galaxy1[1], galaxy2[1])
            for line in self.empty_lines
        ) * (expand_by - 1)
        sum_distances += sum(
            min(galaxy1[0], galaxy2[0]) < col < max(galaxy1[0], galaxy2[0])
            for col in self.empty_cols
        ) * (expand_by - 1)
        return sum_distances


def level11(expand_by: int) -> int:
    universe = parse_input_file()
    sum_distances = 0
    for i in range(0, len(universe.galaxies)):
        galaxy1 = universe.galaxies[i]
        for galaxy2 in universe.galaxies[(i+1):]:
            sum_distances += universe.get_distance(galaxy1, galaxy2, expand_by)
    return sum_distances


def parse_input_file() -> Universe:
    lines = read_input_file(11)
    return Universe(lines)


if __name__ == '__main__':
    print("Sum distances (expand 2): " + str(level11(2)))
    print("Sum distances (expand 1000000): " + str(level11(1000000)))


def test_level11():
    assert 374 == level11(2)
    assert 1030 == level11(10)
    assert 8410 == level11(100)
