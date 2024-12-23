from enum import Enum

from util.data_util import convert_string_list
from util.file_util import read_input_file
from util.math_util import Area, NEWSDirections, Position
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    Reachable = "+"
    Rock = "#"
    Start = "S"


PARITY_0 = 0
PARITY_1 = 1


def parse_input_file() -> Area:
    lines = read_input_file(21)
    return Area(convert_string_list(lines, Field))


def level21_finite(steps: int) -> int:
    area = parse_input_file()
    start = area.find_first(Field.Start)
    area[start] = Field.Free

    reached_fields = {start}
    for _ in range(steps):
        new_reached_fields = set()
        for position in reached_fields:
            for direction in NEWSDirections:
                if area.safe_check(position + direction, Field.Free):
                    new_reached_fields.add(position + direction)
        reached_fields = new_reached_fields

    return len(reached_fields)


def calc_reachable_fields(area: Area, start: Position, steps: int) -> list[int]:
    reachable_fields: list[int] = [0, 0]
    for position in area:
        distance = (position - start).get_orthogonal_length()
        if area[position] == Field.Reachable and distance <= steps:
            parity = (position.x + position.y) % 2
            reachable_fields[parity] += 1
    return reachable_fields


def level21_infinite(steps: int) -> int:
    area = parse_input_file()
    start = area.find_first(Field.Start)
    area[start] = Field.Free
    area.flood_fill(start, Field.Reachable)

    full = calc_reachable_fields(area, start, 130)

    top_left_big = calc_reachable_fields(area, Position(131, 131), 197)[PARITY_0]
    top_right_big = calc_reachable_fields(area, Position(-1, 131), 197)[PARITY_0]
    bottom_right_big = calc_reachable_fields(area, Position(-1, -1), 197)[PARITY_0]
    bottom_left_big = calc_reachable_fields(area, Position(131, -1), 197)[PARITY_0]

    top_left_small = calc_reachable_fields(area, Position(131, 131), 66)[PARITY_1]
    top_right_small = calc_reachable_fields(area, Position(-1, 131), 66)[PARITY_1]
    bottom_right_small = calc_reachable_fields(area, Position(-1, -1), 66)[PARITY_1]
    bottom_left_small = calc_reachable_fields(area, Position(131, -1), 66)[PARITY_1]

    top_mid = calc_reachable_fields(area, Position(start.x, 131), 131)[PARITY_0]
    left_mid = calc_reachable_fields(area, Position(131, start.y), 131)[PARITY_0]
    bottom_mid = calc_reachable_fields(area, Position(start.x, -1), 131)[PARITY_0]
    right_mid = calc_reachable_fields(area, Position(-1, start.y), 131)[PARITY_0]

    side_length_green = (steps - 65) // 131 - 1
    side_length_blue = (steps - 65) // 131
    return (top_mid + left_mid + bottom_mid + right_mid +
            full[PARITY_1] * side_length_blue * side_length_blue + full[PARITY_0] * side_length_green * side_length_green +
            (top_left_small + top_right_small + bottom_right_small + bottom_left_small) * side_length_blue +
            (top_left_big + top_right_big + bottom_right_big + bottom_left_big) * side_length_green)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num reached fields: {level21_finite(64)}")
    print(f"Num reached fields: {level21_infinite(26501365)}")
    timer.print()


def test_level21():
    assert level21_finite(6) == 16
