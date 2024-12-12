from collections import defaultdict
from enum import Enum
from math import sqrt

from util.file_util import read_input_file
from util.math_util import Direction, Position, Area, create_2d_list, is_turn_right, is_turn_left, clamp
from util.run_util import RunTimer

direction_translate = {
    "U": Direction.North,
    "R": Direction.East,
    "D": Direction.South,
    "L": Direction.West,
    "3": Direction.North,
    "0": Direction.East,
    "1": Direction.South,
    "2": Direction.West
}


class Command:
    direction: Direction
    distance: int

    def __init__(self, line: str, flip: bool = False):
        parts = line.split(" ")
        if not flip:
            self.direction = direction_translate[parts[0]]
            self.distance = int(parts[1])
        else:
            self.direction = direction_translate[parts[2][-2]]
            self.distance = int(parts[2][2:-2], 16)

    def __str__(self):
        return f"Command({self.direction} * {self.distance})"


class Field(Enum):
    Not_Dug = "."
    Dug = "#"


def parse_input_file(flip: bool) -> list[Command]:
    return list(map(lambda x: Command(x, flip), read_input_file(18)))


# not used, b ut left in for nostalgia
def level18_flood_fill(flip: bool) -> int:
    commands = parse_input_file(flip)
    position = Position(0, 0)
    min_position = Position(0, 0)
    max_position = Position(0, 0)
    for command in commands:
        position += command.direction * command.distance
        min_position.x = min(position.x, min_position.x)
        min_position.y = min(position.y, min_position.y)
        max_position.x = max(position.x, max_position.x)
        max_position.y = max(position.y, max_position.y)

    dimensions = max_position - min_position
    field = create_2d_list(dimensions.x + 1, dimensions.y + 1, Field.Not_Dug)
    area = Area(field)

    start = -min_position
    position = start.copy()
    old_command = None
    num_right_turns = 0
    num_left_turns = 0
    for i in range(len(commands)):
        command = commands[i]
        if old_command is not None:
            if is_turn_right(old_command.direction, command.direction):
                num_right_turns += 1
            elif is_turn_left(old_command.direction, command.direction):
                num_left_turns -= 1

        for _ in range(command.distance):
            area[position] = Field.Dug
            position += command.direction

        old_command = command

    flood_fill_start = start.copy()
    flood_fill_start += commands[0].direction
    if num_right_turns > num_left_turns:
        flood_fill_start += commands[0].direction.turn_right_90()
    else:
        flood_fill_start += commands[0].direction.turn_left_90()
    area.flood_fill(flood_fill_start, Field.Dug)

    area.print()
    return area.count(Field.Dug)


class Vertex:
    start: Position
    end: Position

    def __init__(self, start: Position, end: Position):
        self.start = start.copy()
        self.end = end.copy()

    def __str__(self) -> str:
        return f"{self.start} -> {self.end}"

    def __len__(self):
        len_x = self.end.x - self.start.x
        len_y = self.end.y - self.start.y
        return int(sqrt(len_x * len_x + len_y * len_y)) + 1


def calc_vertices(commands: list[Command]) -> tuple[dict[int, list[Vertex]], dict[int, list[Vertex]]]:
    start = Position(0, 0)
    horizontal_vertices = []
    vertical_vertices = []

    for command in commands:
        end = start + command.direction * command.distance
        if command.direction == Direction.East or command.direction == Direction.West:
            horizontal_vertices.append(Vertex(start, end))
        else:
            vertical_vertices.append(Vertex(start, end))
        start = end

    horizontal_vertices.sort(key=lambda v: v.start.y)
    vertical_vertices.sort(key=lambda v: v.start.x)

    horizontal_vertex_dict = defaultdict(list)
    for vertex in horizontal_vertices:
        horizontal_vertex_dict[vertex.start.y].append(vertex)

    vertical_vertex_dict = defaultdict(list)
    for vertex in vertical_vertices:
        vertical_vertex_dict[vertex.start.x].append(vertex)
    return horizontal_vertex_dict, vertical_vertex_dict


def slice_to_grid(horizontal_vertices: dict[int, list[Vertex]], vertical_vertices: dict[int, list[Vertex]]) -> tuple[list[int], list[int]]:
    horizontal_slices = []
    for x in vertical_vertices:
        horizontal_slices.append(x)

    vertical_slices = []
    for y in horizontal_vertices:
        vertical_slices.append(y)

    return horizontal_slices, vertical_slices


def enters_or_leaves_area(was_in_area: bool, x: int, y: int, horizontal_vertex_dict: dict[int, list[Vertex]], vertical_vertices: dict[int, list[Vertex]]) -> bool:
    for vertex in vertical_vertices[x]:
        if vertex.start.x == x and (vertex.start.y <= y <= vertex.end.y or vertex.end.y <= y <= vertex.start.y):
            if not was_in_area:
                enters_or_leaves_area.was_in_before_edge = was_in_area
                enters_or_leaves_area.last_vertex_hit = vertex
                return True

            for horizontal_vertex in horizontal_vertex_dict[y]:
                if horizontal_vertex.start.x == x or horizontal_vertex.end.x == x:
                    max_x = max(horizontal_vertex.start.x, horizontal_vertex.end.x)
                    if max_x == x:
                        min_y_now = min(vertex.start.y, vertex.end.y)
                        max_y_now = max(vertex.start.y, vertex.end.y)
                        min_y_before = min(enters_or_leaves_area.last_vertex_hit.start.y, enters_or_leaves_area.last_vertex_hit.end.y)
                        max_y_before = max(enters_or_leaves_area.last_vertex_hit.start.y, enters_or_leaves_area.last_vertex_hit.end.y)
                        enters_or_leaves_area.last_vertex_hit = vertex
                        if min_y_now == min_y_before or max_y_now == max_y_before:
                            return not enters_or_leaves_area.was_in_before_edge
                        else:
                            return enters_or_leaves_area.was_in_before_edge
                    else:
                        enters_or_leaves_area.was_in_before_edge = was_in_area
                        enters_or_leaves_area.last_vertex_hit = vertex
                        return False
            enters_or_leaves_area.last_vertex_hit = vertex
            return True
    return False


def calc_area(y: int, height: int, horizontal_slices: list[int], horizontal_vertex_dict: dict[int, list[Vertex]], vertical_vertices: dict[int, list[Vertex]]) -> int:
    area = 0
    is_in_area = False

    enters_or_leaves_area.last_vertex_hit = None
    enters_or_leaves_area.was_in_before_edge = False

    for x in range(len(horizontal_slices)):
        horizontal_slice = horizontal_slices[x]
        was_in_area = is_in_area
        if enters_or_leaves_area(is_in_area, horizontal_slice, y, horizontal_vertex_dict, vertical_vertices):
            is_in_area = not is_in_area
        if is_in_area:
            if x == len(horizontal_slices) - 1:
                area += 1
            else:
                next_horizontal_slice = horizontal_slices[x + 1]
                width = next_horizontal_slice - horizontal_slice
                area += width * height
        elif was_in_area:
            area += height
    return area


def level18(flip: bool) -> int:
    commands = parse_input_file(flip)
    horizontal_vertices, vertical_vertices = calc_vertices(commands)
    horizontal_slices, vertical_slices = slice_to_grid(horizontal_vertices, vertical_vertices)

    area = 0
    for y in range(len(vertical_slices)):
        vertical_slice = vertical_slices[y]
        area += calc_area(vertical_slice, 1, horizontal_slices, horizontal_vertices, vertical_vertices)
        if y != len(vertical_slices) - 1:
            next_vertical_slice = vertical_slices[y + 1]
            height = next_vertical_slice - vertical_slice - 1
            if height != 0:
                area += calc_area(vertical_slice + 1, height, horizontal_slices, horizontal_vertices, vertical_vertices)

    return area


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Lave lake size: {level18(False)}, {level18(True)}")
    timer.print()


def test_level18():
    assert (level18(False), level18(True)) == (62, 952408144115)
