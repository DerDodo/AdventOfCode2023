from enum import Enum

from util.file_util import read_input_file_id


class CantStepException(Exception): pass
class InvalidDirectionsException(Exception): pass


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
                "S": None,
                "|": Direction.North,
                "7": Direction.West,
                "F": Direction.East,
            },
            Direction.East: {
                "S": None,
                "-": Direction.East,
                "J": Direction.North,
                "7": Direction.South,
            },
            Direction.South: {
                "S": None,
                "|": Direction.South,
                "L": Direction.East,
                "J": Direction.West,
            },
            Direction.West: {
                "S": None,
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
            new_value = self.pipes[new_y][new_x]
            return new_value == "S" or new_value != "|" or new_value != "7" or new_value != "F"
        elif direction == Direction.East and new_x != len(self.pipes[0]):
            new_value = self.pipes[new_y][new_x]
            return new_value == "S" or new_value != "-" or new_value != "J" or new_value != "7"
        elif direction == Direction.South and new_y != len(self.pipes):
            new_value = self.pipes[new_y][new_x]
            return new_value == "S" or new_value != "|" or new_value != "L" or new_value != "J"
        elif direction == Direction.West and new_x != -1:
            new_value = self.pipes[new_y][new_x]
            return new_value == "S" or new_value != "-" or new_value != "L" or new_value != "F"
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

    def get_loop_direction(self) -> LoopDirection | None:
        direction_diff = self.new_direction.value - self.old_direction.value

        if direction_diff == 1 or direction_diff == -3:
            return LoopDirection.Right
        elif direction_diff == -1 or direction_diff == 3:
            return LoopDirection.Left
        else:
            return None

    def get_fill_tiles(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if self.value == "|":
            return self.__get_fill_tiles_for_bar(loop_direction)
        elif self.value == "-":
            return self.__get_fill_tiles_for_minus(loop_direction)
        elif self.value == "L":
            return self.__get_fill_tiles_for_l(loop_direction)
        elif self.value == "J":
            return self.__get_fill_tiles_for_j(loop_direction)
        elif self.value == "7":
            return self.__get_fill_tiles_for_7(loop_direction)
        elif self.value == "F":
            return self.__get_fill_tiles_for_f(loop_direction)
        elif self.value == "S":
            return self.__get_fill_tiles_for_s(loop_direction)
        return []

    def __get_fill_tiles_for_bar(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if ((loop_direction == LoopDirection.Right and self.new_direction == Direction.North)
                or (loop_direction == LoopDirection.Left and self.new_direction == Direction.South)):
            return [(1, 0)]
        else:
            return [(-1, 0)]

    def __get_fill_tiles_for_minus(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if ((loop_direction == LoopDirection.Right and self.new_direction == Direction.West)
                or (loop_direction == LoopDirection.Left and self.new_direction == Direction.East)):
            return [(0, -1)]
        else:
            return [(0, 1)]

    def __get_fill_tiles_for_l(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if ((loop_direction == LoopDirection.Right and self.new_direction == Direction.East)
                or (loop_direction == LoopDirection.Left and self.new_direction == Direction.North)):
            return [(0, 1), (-1, 0)]
        else:
            return []

    def __get_fill_tiles_for_j(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if ((loop_direction == LoopDirection.Right and self.new_direction == Direction.North)
                or (loop_direction == LoopDirection.Left and self.new_direction == Direction.West)):
            return [(0, 1), (1, 0)]
        else:
            return []

    def __get_fill_tiles_for_7(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if ((loop_direction == LoopDirection.Right and self.new_direction == Direction.West)
                or (loop_direction == LoopDirection.Left and self.new_direction == Direction.South)):
            return [(0, -1), (1, 0)]
        else:
            return []

    def __get_fill_tiles_for_f(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if ((loop_direction == LoopDirection.Right and self.new_direction == Direction.South)
                or (loop_direction == LoopDirection.Left and self.new_direction == Direction.East)):
            return [(0, -1), (-1, 0)]
        else:
            return []

    def __get_fill_tiles_for_s(self, loop_direction: LoopDirection) -> list[tuple[int, int]]:
        if loop_direction == LoopDirection.Right:
            if self.new_direction == Direction.North:
                return [(1, 0)]
            elif self.new_direction == Direction.East:
                return [(0, 1)]
            elif self.new_direction == Direction.South:
                return [(-1, 0)]
            else:
                return [(0, -1)]
        else:
            if self.new_direction == Direction.North:
                return [(-1, 0)]
            elif self.new_direction == Direction.East:
                return [(0, -1)]
            elif self.new_direction == Direction.South:
                return [(1, 0)]
            else:
                return [(0, 1)]


class FillLabyrinth:
    area: list[list[str]]
    loop_tiles: list[LoopTile]
    loop_direction: LoopDirection

    __clear_tile = "."
    __inside_tile = "*"

    def __init__(self, labyrinth: Labyrinth, loop_tiles: list[LoopTile]):
        self.area = [[self.__clear_tile for _ in labyrinth.pipes[0]] for _ in labyrinth.pipes[0]]
        self.loop_tiles = loop_tiles

        for loop_tile in loop_tiles:
            self.area[loop_tile.y][loop_tile.x] = loop_tile.value

        self.loop_direction = self.__calc_loop_direction()

        for loop_tile in loop_tiles[0:-1]:
            to_fill = loop_tile.get_fill_tiles(self.loop_direction)
            for field in to_fill:
                self.__flood_fill_inside(loop_tile.x + field[0], loop_tile.y + field[1])

    def __calc_loop_direction(self) -> LoopDirection:
        num_turns = {direction: 0 for direction in LoopDirection}
        num_turns[None] = 0

        for loop_tile in self.loop_tiles:
            num_turns[loop_tile.get_loop_direction()] += 1

        if num_turns[LoopDirection.Right] > num_turns[LoopDirection.Left]:
            return LoopDirection.Right
        else:
            return LoopDirection.Left
        
    def __flood_fill_inside(self, x: int, y: int):
        if not self.should_flood_fill(x, y):
            return
        self.area[y][x] = self.__inside_tile
        self.__flood_fill_inside(x - 1, y)
        self.__flood_fill_inside(x + 1, y)
        self.__flood_fill_inside(x, y + 1)
        self.__flood_fill_inside(x, y - 1)

    def should_flood_fill(self, x: int, y: int):
        return 0 <= x < len(self.area[0]) and 0 <= y < len(self.area) and self.area[y][x] == self.__clear_tile

    def get_num_tiles_inside(self) -> int:
        return sum(map(lambda line: line.count(self.__inside_tile), self.area))


def level10(file_id: int) -> tuple[int, int]:
    labyrinth = parse_input_file(file_id)
    loop_tiles = calc_loop(labyrinth)
    fill_labyrinth = FillLabyrinth(labyrinth, loop_tiles)
    return int((len(loop_tiles)) / 2), fill_labyrinth.get_num_tiles_inside()


def parse_input_file(file_id: int) -> Labyrinth:
    lines = read_input_file_id(10, file_id)
    return Labyrinth(lines)


def calc_loop(labyrinth: Labyrinth) -> list[LoopTile]:
    start_x, start_y = find_start(labyrinth)
    for start_direction in Direction:
        x, y, direction = start_x, start_y, start_direction
        loop_tiles = []
        for _ in range(0, 100000):
            try:
                old_direction = direction
                x, y, direction = labyrinth.step(x, y, direction)
                if labyrinth.pipes[y][x] == "S":
                    loop_tiles.append(LoopTile(x, y, old_direction, start_direction, labyrinth.pipes[y][x]))
                    return loop_tiles
                loop_tiles.append(LoopTile(x, y, old_direction, direction, labyrinth.pipes[y][x]))
            except CantStepException:
                break


def find_start(labyrinth: Labyrinth) -> tuple[int, int]:
    found_s = list(map(lambda line: line.find("S"), labyrinth.pipes))
    start_y = [idx for idx, value in enumerate(found_s) if value != -1][0]
    start_x = found_s[start_y]
    return start_x, start_y


if __name__ == '__main__':
    print("Longest distance, tiles inside: " + str(level10(4)))


def test_level10():
    assert (4, 1) == level10(0)
    assert (8, 1) == level10(1)
    assert (23, 4) == level10(2)
    assert (70, 8) == level10(3)
    assert (6768, 351) == level10(4)
