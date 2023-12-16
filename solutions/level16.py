from enum import Enum

from util.file_util import read_input_file


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Field:
    definition: list[str]
    visited_fields = list[list[bool]]
    visited_fields_lookup = set[int]

    def __init__(self, definition: list[str]):
        self.definition = definition
        self.visited_fields = [[False] * len(definition[0]) for _ in range(0, len(definition))]
        self.visited_fields_lookup = set()

    def visit(self, x: int, y: int, direction: Direction):
        self.visited_fields[y][x] = True
        self.visited_fields_lookup.add(self.__get_beam_id(x, y, direction))

    def get_energy_level(self) -> int:
        return sum(map(lambda line: sum([t for t in line]), self.visited_fields))

    def __get_beam_id(self, x: int, y: int, direction: Direction) -> int:
        return (y * len(self.definition[0]) + x) * 10 + direction.value

    def was_visited(self, x: int, y: int, direction: Direction) -> bool:
        return self.__get_beam_id(x, y, direction) in self.visited_fields_lookup


class Beam:
    field: Field
    x: int
    y: int
    direction: Direction

    def __init__(self, field: Field, x: int, y: int, direction: Direction):
        self.field = field
        self.x = x
        self.y = y
        self.direction = direction

    def is_still_in_field(self):
        if self.direction == Direction.UP:
            return self.y >= 0
        elif self.direction == Direction.LEFT:
            return self.x >= 0
        elif self.direction == Direction.DOWN:
            return self.y < len(self.field.definition)
        else:
            return self.x < len(self.field.definition[0])

    def move(self):
        char = self.field.definition[self.y][self.x]
        if char == ".":
            self.__move_empty()
            return None
        elif char == "-" or char == "|":
            return self.__move_splitter(char)
        elif char == "/" or char == "\\":
            self.__move_mirror(char)
            return None

    def __move_empty(self):
        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        else:
            self.x += 1

    def __move_splitter(self, char: str):
        if self.direction == Direction.LEFT or self.direction == Direction.RIGHT:
            if char == "-":
                self.__move_empty()
                return None
            else:
                self.direction = Direction.UP
                self.y -= 1
                return Beam(self.field, self.x, self.y + 1, Direction.DOWN)
        else:
            if char == "|":
                self.__move_empty()
                return None
            else:
                self.direction = Direction.LEFT
                self.x -= 1
                return Beam(self.field, self.x + 1, self.y, Direction.RIGHT)

    def __move_mirror(self, char: str):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT if char == "/" else Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN if char == "/" else Direction.UP
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT if char == "/" else Direction.RIGHT
        else:
            self.direction = Direction.UP if char == "/" else Direction.DOWN
        self.__move_empty()


def level16() -> tuple[int, int]:
    field = parse_input_file()
    top_left_to_right = level16_attempt(Beam(field, 0, 0, Direction.RIGHT))
    top_right_to_left = level16_attempt(Beam(field, len(field.definition[0]) - 1, 0, Direction.LEFT))
    max_energy_level = max(top_left_to_right, top_right_to_left)
    for y in range(1, len(field.definition)):
        max_energy_level = max(max_energy_level,
                               level16_attempt(Beam(field, 0, y, Direction.RIGHT)),
                               level16_attempt(Beam(field, len(field.definition[0]) - 1, y, Direction.LEFT))
                               )
    for x in range(0, len(field.definition)):
        max_energy_level = max(max_energy_level,
                               level16_attempt(Beam(field, x, 0, Direction.DOWN)),
                               level16_attempt(Beam(field, x, len(field.definition) - 1, Direction.UP))
                               )
    return top_left_to_right, max_energy_level


def level16_attempt(starting_beam: Beam) -> int:
    field = parse_input_file()
    beams = [starting_beam]
    beam_i = 0
    while beam_i < len(beams):
        beam = beams[beam_i]
        while beam.is_still_in_field() and not field.was_visited(beam.x, beam.y, beam.direction):
            field.visit(beam.x, beam.y, beam.direction)
            new_beam = beam.move()
            if new_beam:
                beams.append(new_beam)
        beam_i += 1
    return field.get_energy_level()


def parse_input_file() -> Field:
    lines = read_input_file(16)
    return Field(lines)


if __name__ == '__main__':
    print("Energized tiles: " + str(level16()))


def test_level16():
    assert (46, 51) == level16()
