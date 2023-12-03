from typing import Tuple

from util.file_util import read_input_file


class EnginePart:
    value: int
    length: int
    x: int
    y: int

    def __init__(self, value: int, length: int, x: int, y: int):
        self.value = value
        self.length = length
        self.x = x
        self.y = y

    def get_neighbors(self, limit_x: int, limit_y: int) -> list[Tuple[int, int]]:
        neighbors = [
            [self.x - 1, self.y - 1],
            [self.x - 1, self.y],
            [self.x - 1, self.y + 1],
            [self.x + self.length, self.y - 1],
            [self.x + self.length, self.y],
            [self.x + self.length, self.y + 1],
        ]

        for i in range(0, self.length):
            neighbors.append([self.x + i, self.y - 1])
            neighbors.append([self.x + i, self.y + 1])

        return list(filter(lambda n: 0 <= n[0] < limit_x and 0 <= n[1] < limit_y, neighbors))


def parse_input_file() -> list[str]:
    return read_input_file(3)


def level3() -> Tuple[int, int]:
    schematic = parse_input_file()
    numbers = find_all_engine_parts(schematic)
    sum_engine_parts, gears = process_numbers(schematic, numbers)
    total_gear_ratio = 0
    for gear in gears.values():
        if len(gear) == 2:
            total_gear_ratio += gear[0] * gear[1]
    return sum_engine_parts, total_gear_ratio


def process_numbers(schematic: list[str], numbers: list[EnginePart]) -> Tuple[int, dict[int, list[int]]]:
    sum_engine_parts = 0
    gears = dict()
    for number in numbers:
        neighbors = number.get_neighbors(len(schematic[0]), len(schematic))
        is_enine_part = False
        for neighbor in neighbors:
            value = schematic[neighbor[1]][neighbor[0]]
            if not value.isdigit() and value != ".":
                is_enine_part = True
            if value == "*":
                coordinate_id = get_coordinate_id(neighbor[0], neighbor[1], len(schematic[0]))
                if coordinate_id not in gears:
                    gears[coordinate_id] = []
                gears[coordinate_id].append(number.value)
        if is_enine_part:
            sum_engine_parts += number.value
    return sum_engine_parts, gears


def find_all_engine_parts(schematic: list[str]) -> list[EnginePart]:
    engine_parts = list()
    max_x = len(schematic[0])
    max_y = len(schematic)
    for y in range(0, max_y):
        number_start = -1
        number = 0
        for x in range(0, max_x):
            if schematic[y][x].isdigit():
                if number_start == -1:
                    number_start = x
                    number = int(schematic[y][x])
                else:
                    number = number * 10 + int(schematic[y][x])
            elif number_start != -1:
                engine_parts.append(EnginePart(number, x - number_start, number_start, y))
                number_start = -1
                number = 0
        if number_start != -1:
            engine_parts.append(EnginePart(number, max_x - number_start, number_start, y))

    return engine_parts


def get_coordinate_id(x: int, y: int, width: int) -> int:
    return y * width + x


if __name__ == '__main__':
    print("Engine part sum: " + str(level3()))


def test_level3():
    assert (4361, 467835) == level3()
