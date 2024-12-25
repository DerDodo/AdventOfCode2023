from collections import deque
from enum import Enum

from util.data_util import create_2d_list, convert_string_list
from util.file_util import read_input_file
from util.math_util import Area, Position, NEWSDirections, Direction
from util.run_util import RunTimer


class Field(Enum):
    Wall = "#"
    Free = "."
    SouthSlope = "v"
    NorthSlope = "^"
    WestSlope = "<"
    EastSlope = ">"

    def get_check_directions(self, can_climb: bool) -> list:
        if self == Field.Wall:
            return []
        elif self == Field.Free or can_climb:
            return NEWSDirections
        elif self == Field.SouthSlope:
            return [Direction.South]
        elif self == Field.NorthSlope:
            return [Direction.North]
        elif self == Field.WestSlope:
            return [Direction.West]
        elif self == Field.EastSlope:
            return [Direction.East]


NOT_WALKED = 9999999999999
NOT_FOUND = -1


class Landscape(Area):
    start: Position
    end: Position

    def __init__(self, lines: list[str]):
        super().__init__(convert_string_list(lines, Field))
        self.start = Position(1, 0)
        self.end = Position(len(self.field) - 2, len(self.field) - 1)

    def find_longest_hike(self, can_climb: bool) -> int:
        crossings = self.find_all_crossings(can_climb)
        last_field = self.find_last_crossing(crossings)
        return self.find_longest_path(crossings, 0, self.start, {self.start.hash_value}, last_field)

    def find_last_crossing(self, crossings: dict[Position, list[tuple[Position, int]]]) -> Position:
        for crossing, ends in crossings.items():
            for end, _ in ends:
                if end == self.end:
                    return crossing

    def find_all_crossings(self, can_climb: bool) -> dict[Position, list[tuple[Position, int]]]:
        crossings: dict[Position, list[tuple[Position, int]]] = dict()
        unchecked_crossings: deque[Position] = deque()
        unchecked_crossings.append(Position(1, 0))

        while unchecked_crossings:
            crossing = unchecked_crossings.popleft()
            next_crossings = self.find_next_crossings(crossing.x, crossing.y, can_climb)
            crossings[crossing] = next_crossings
            for next_crossing in next_crossings:
                if next_crossing[0] not in crossings:
                    unchecked_crossings.append(next_crossing[0])

        return crossings

    def find_next_crossings(self, x: int, y: int, can_climb: bool) -> list[tuple[Position, int]]:
        crossings = []

        paths = Area(create_2d_list(self.bounds.x, self.bounds.y, NOT_WALKED))
        paths.field[y][x] = 0

        paths_to_follow = deque()
        paths_to_follow.extend(self._a_star_calc_next_steps(paths, 0, x, y, can_climb))

        while paths_to_follow:
            score, position = paths_to_follow.popleft()
            if score < paths.field[position.y][position.x]:
                paths.field[position.y][position.x] = score

                if (position.x == self.end.x and position.y == self.end.y) or (position.x == self.start.x and position.y == self.start.y):
                    crossings.append((position, score))
                else:
                    next_paths = self._a_star_calc_next_steps(paths, score, position.x, position.y, can_climb)
                    if len(next_paths) > 1:
                        crossings.append((position, score))
                    else:
                        paths_to_follow.extend(next_paths)
        return crossings

    def _a_star_calc_next_steps(self, paths: Area, score: int, x: int, y: int, can_climb: bool) -> set[tuple[int, Position]]:
        next_steps = set()
        check_directions = self.field[y][x].get_check_directions(can_climb)

        for direction in check_directions:
            new_score = score + 1
            new_x = x + direction.x
            new_y = y + direction.y
            if 0 <= new_x < self.bounds.x and 0 <= new_y < self.bounds.y and self.field[new_y][new_x] != Field.Wall and score < paths.field[new_y][new_x]:
                next_steps.add((new_score, Position(new_x, new_y)))
        return next_steps

    def find_longest_path(self, crossings: dict[Position, list[tuple[Position, int]]], score: int, crossing: Position, used_crossings: set[int], last_field: Position) -> int:
        if crossing.x == last_field.x and crossing.y == last_field.y:
            for next_crossing in crossings[last_field]:
                if next_crossing[0] == self.end:
                    return score + crossings[last_field][0][1]

        max_score = NOT_FOUND
        for next_crossing in crossings[crossing]:
            if next_crossing[0].hash_value not in used_crossings:
                new_score = self.find_longest_path(crossings, score + next_crossing[1], next_crossing[0], {*used_crossings, next_crossing[0].hash_value}, last_field)
                max_score = max(max_score, new_score)

        return max_score


def parse_input_file() -> Landscape:
    lines = read_input_file(23)
    return Landscape(lines)


def level23() -> tuple[int, int]:
    landscape = parse_input_file()
    return landscape.find_longest_hike(False), landscape.find_longest_hike(True)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Longest hike: {level23()}")
    timer.print()


def test_level21():
    assert level23() == (94, 154)
