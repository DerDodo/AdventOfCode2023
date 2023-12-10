from enum import Enum

from util.file_util import read_input_file_id


class CantStepException(Exception):
    pass


class LoopDirection(Enum):
    Left = 0
    Right = 1


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

    def step(self, x, y) -> tuple[int, int]:
        if self == Direction.North:
            return x, y - 1
        elif self == Direction.East:
            return x + 1, y
        elif self == Direction.South:
            return x, y + 1
        else:
            return x - 1, y


class Labyrinth:
    pipes: list[str]
    direction_translate = dict[Direction, dict[str, Direction]]

    def __init__(self, definition: list[str]):
        self.pipes = definition
        self.direction_translate = {
            Direction.North: {
                "S": Direction.North,
                "|": Direction.North,
                "7": Direction.West,
                "F": Direction.East,
            },
            Direction.East: {
                "S": Direction.East,
                "-": Direction.East,
                "J": Direction.North,
                "7": Direction.South,
            },
            Direction.South: {
                "S": Direction.South,
                "|": Direction.South,
                "L": Direction.East,
                "J": Direction.West,
            },
            Direction.West: {
                "S": Direction.West,
                "-": Direction.West,
                "L": Direction.North,
                "F": Direction.South,
            },
        }

    def step(self, x, y, direction) -> tuple[int, int, Direction]:
        if not self.can_step(x, y, direction):
            raise CantStepException
        new_x, new_y = direction.step(x, y)
        new_value = self.pipes[new_y][new_x]
        if new_value not in self.direction_translate[direction]:
            raise CantStepException
        return new_x, new_y, self.direction_translate[direction][new_value]

    def can_step(self, x, y, direction) -> bool:
        new_x, new_y = direction.step(x, y)
        if direction == Direction.North and new_y != -1:
            value = self.pipes[new_y][new_x]
            return value == "S" or value != "|" or value != "7" or value != "F"
        elif direction == Direction.East and new_x != len(self.pipes[0]):
            value = self.pipes[new_y][new_x]
            return value == "S" or value != "-" or value != "J" or value != "7"
        elif direction == Direction.South and new_y != len(self.pipes):
            value = self.pipes[new_y][new_x]
            return value == "S" or value != "|" or value != "L" or value != "J"
        elif direction == Direction.West and new_x != -1:
            value = self.pipes[new_y][new_x]
            return value == "S" or value != "-" or value != "L" or value != "F"
        return False


class LoopTile:
    x: int
    y: int
    old_direction: Direction
    new_direction: Direction
    value: str

    def __init__(self, x, y, old_direction, new_direction, value):
        self.x = x
        self.y = y
        self.old_direction = old_direction
        self.new_direction = new_direction
        self.value = value


class FillLabyrinth:
    area: list[list[str]]
    loop_direction: LoopDirection
    fill_tiles: dict[LoopDirection, dict[str, dict[Direction, list[tuple[int, int]]]]]

    __clear_tile = "."
    __inside_tile = "*"

    def __init__(self, labyrinth: Labyrinth, loop_tiles: list[LoopTile]):
        self.area = [[self.__clear_tile for _ in labyrinth.pipes[0]] for _ in labyrinth.pipes[0]]

        self.fill_tiles = {
            LoopDirection.Right: {
                "|": {
                    Direction.North: [(1, 0)],
                    Direction.South: [(-1, 0)],
                },
                "-": {
                    Direction.West: [(0, -1)],
                    Direction.East: [(0, 1)],
                },
                "L": {
                    Direction.North: [],
                    Direction.East: [(0, 1), (-1, 0)],
                },
                "J": {
                    Direction.North: [(0, 1), (1, 0)],
                    Direction.West: [],
                },
                "7": {
                    Direction.South: [],
                    Direction.West: [(0, -1), (1, 0)],
                },
                "F": {
                    Direction.East: [],
                    Direction.South: [(0, -1), (-1, 0)],
                },
                "S": {
                    Direction.North: [(1, 0)],
                    Direction.East: [(0, 1)],
                    Direction.South: [(-1, 0)],
                    Direction.West: [(0, -1)],
                }
            },
            LoopDirection.Left: {
                "|": {
                    Direction.South: [(1, 0)],
                    Direction.North: [(-1, 0)],
                },
                "-": {
                    Direction.East: [(0, -1)],
                    Direction.West: [(0, 1)],
                },
                "L": {
                    Direction.East: [],
                    Direction.North: [(0, 1), (-1, 0)],
                },
                "J": {
                    Direction.West: [(0, 1), (1, 0)],
                    Direction.North: [],
                },
                "7": {
                    Direction.West: [],
                    Direction.South: [(0, -1), (1, 0)],
                },
                "F": {
                    Direction.South: [],
                    Direction.East: [(0, -1), (-1, 0)],
                },
                "S": {
                    Direction.South: [(1, 0)],
                    Direction.West: [(0, 1)],
                    Direction.North: [(-1, 0)],
                    Direction.East: [(0, -1)],
                }
            }
        }

        num_right_turns = 0
        num_left_turns = 0
        for loop_tile in loop_tiles:
            self.area[loop_tile.y][loop_tile.x] = loop_tile.value

            if loop_tile.value == "S":
                direction_diff = loop_tiles[0].new_direction.value - loop_tiles[-1].new_direction.value
            else:
                direction_diff = loop_tile.new_direction.value - loop_tile.old_direction.value
            if direction_diff == 1 or direction_diff == -3:
                num_right_turns += 1
            elif direction_diff == -1 or direction_diff == 3:
                num_left_turns += 1

        if num_right_turns > num_left_turns:
            self.loop_direction = LoopDirection.Right
        else:
            self.loop_direction = LoopDirection.Left

        for loop_tile in loop_tiles:
            to_fill = self.fill_tiles[self.loop_direction][loop_tile.value][loop_tile.new_direction]
            for field in to_fill:
                self.flood_fill_inside(loop_tile.x + field[0], loop_tile.y + field[1])

    def flood_fill_inside(self, x: int, y: int):
        if not self.should_flood_fill(x, y):
            return
        self.area[y][x] = self.__inside_tile
        self.flood_fill_inside(x - 1, y)
        self.flood_fill_inside(x + 1, y)
        self.flood_fill_inside(x, y + 1)
        self.flood_fill_inside(x, y - 1)

    def should_flood_fill(self, x: int, y: int):
        return 0 <= x < len(self.area[0]) and 0 <= y < len(self.area) and self.area[y][x] == self.__clear_tile

    def get_num_tiles_inside(self) -> int:
        return sum(map(lambda line: line.count(self.__inside_tile), self.area))


def level10(file_id: int) -> tuple[int, int]:
    labyrinth = parse_input_file(file_id)
    found_s = list(map(lambda line: line.find("S"), labyrinth.pipes))
    start_y = [idx for idx, value in enumerate(found_s) if value != -1][0]
    start_x = found_s[start_y]
    loop_tiles = None
    longest_distance = -1
    for start_direction in Direction:
        x = start_x
        y = start_y
        test_loop_tiles: list[LoopTile] = [LoopTile(x, y, None, start_direction, labyrinth.pipes[y][x])]
        direction = start_direction
        for num_steps in range(0, 1000000):
            try:
                new_x, new_y, new_direction = labyrinth.step(x, y, direction)
                old_direction = direction
                x, y, direction = new_x, new_y, new_direction
                test_loop_tiles.append(LoopTile(x, y, old_direction, direction, labyrinth.pipes[y][x]))
                if x == start_x and y == start_y:
                    loop_tiles = test_loop_tiles
                    longest_distance = int((num_steps + 1) / 2)
                    break
            except CantStepException:
                break
        if longest_distance != -1:
            break
    fill_labyrinth = FillLabyrinth(labyrinth, loop_tiles)
    return longest_distance, fill_labyrinth.get_num_tiles_inside()


def parse_input_file(file_id: int) -> Labyrinth:
    lines = read_input_file_id(10, file_id)
    return Labyrinth(lines)


if __name__ == '__main__':
    print("Longest distance, tiles inside: " + str(level10(4)))


def test_level10():
    assert (4, 1) == level10(0)
    assert (8, 1) == level10(1)
    assert (23, 4) == level10(2)
    assert (70, 8) == level10(3)
