import math
from enum import Enum


def count_digits(n) -> int:
    if n == 0:
        return 1

    return math.floor(math.log10(abs(n))) + 1


def clamp(n):
    return max(-1, min(1, n))


class Direction(Enum):
    North = 0, -1
    NorthEast = 1, -1
    East = 1, 0
    SouthEast = 1, 1
    South = 0, 1
    SouthWest = -1, 1
    West = -1, 0
    NorthWest = -1, -1

    x: int
    y: int
    hash_value: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        # runtime optimization
        self.hash_value = (y + 1) * 3 + x + 1

    @staticmethod
    def from_arrow(arrow: str):
        if arrow == "^":
            return Direction.North
        elif arrow == ">":
            return Direction.East
        elif arrow == "v":
            return Direction.South
        elif arrow == "<":
            return Direction.West
        else:
            raise ValueError(f"Invalid direction arrow '{arrow}'")

    def turn_left_90(self):
        match self:
            case Direction.North:
                return Direction.West
            case Direction.NorthEast:
                return Direction.NorthWest
            case Direction.East:
                return Direction.North
            case Direction.SouthEast:
                return Direction.NorthEast
            case Direction.South:
                return Direction.East
            case Direction.SouthWest:
                return Direction.SouthEast
            case Direction.West:
                return Direction.South
            case Direction.NorthWest:
                return Direction.SouthWest

    def turn_right_90(self):
        match self:
            case Direction.North:
                return Direction.East
            case Direction.NorthEast:
                return Direction.SouthEast
            case Direction.East:
                return Direction.South
            case Direction.SouthEast:
                return Direction.SouthWest
            case Direction.South:
                return Direction.West
            case Direction.SouthWest:
                return Direction.NorthWest
            case Direction.West:
                return Direction.North
            case Direction.NorthWest:
                return Direction.NorthEast

    def __mul__(self, other):
        if isinstance(other, int):
            return self.x * other, self.y * other
        raise TypeError(f"{other} is no int")

    def __hash__(self) -> int:
        return self.hash_value

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(f"Invalid index {index}")

    def __setitem__(self, index: int, value: int):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(f"Invalid index {index}")


def is_turn_right(old: Direction, new: Direction) -> bool:
    match old:
        case Direction.North:
            return new == Direction.East
        case Direction.NorthEast:
            return new == Direction.SouthEast
        case Direction.East:
            return new == Direction.South
        case Direction.SouthEast:
            return new == Direction.SouthWest
        case Direction.South:
            return new == Direction.West
        case Direction.SouthWest:
            return new == Direction.NorthWest
        case Direction.West:
            return new == Direction.North
        case Direction.NorthWest:
            return new == Direction.NorthEast


def is_turn_left(old: Direction, new: Direction) -> bool:
    match old:
        case Direction.North:
            return new == Direction.West
        case Direction.NorthEast:
            return new == Direction.NorthWest
        case Direction.East:
            return new == Direction.North
        case Direction.SouthEast:
            return new == Direction.NorthEast
        case Direction.South:
            return new == Direction.East
        case Direction.SouthWest:
            return new == Direction.SouthEast
        case Direction.West:
            return new == Direction.South
        case Direction.NorthWest:
            return new == Direction.SouthWest



class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x != other.x or self.y != other.y
        return True

    def __add__(self, other):
        if isinstance(other, Position) or isinstance(other, Direction):
            return Position(self.x + other.x, self.y + other.y)
        if isinstance(other, int):
            return Position(self.x + other, self.y + other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x + other[0], self.y + other[1])
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __iadd__(self, other):
        if isinstance(other, Position) or isinstance(other, Direction):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int):
            self.x += other
            self.y += other
        elif isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            self.x += other[0]
            self.y += other[1]
        else:
            raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")
        return self

    def __sub__(self, other):
        if isinstance(other, Position) or isinstance(other, Direction):
            return Position(self.x - other.x, self.y - other.y)
        if isinstance(other, int):
            return Position(self.x - other, self.y - other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x - other[0], self.y - other[1])
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __isub__(self, other):
        if isinstance(other, Position) or isinstance(other, Direction):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int):
            self.x -= other
            self.y -= other
        elif isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            self.x -= other[0]
            self.y -= other[1]
        else:
            raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")
        return self

    def __mul__(self, other):
        if isinstance(other, Position) or isinstance(other, Direction):
            return Position(self.x * other.x, self.y * other.y)
        if isinstance(other, int):
            return Position(self.x * other, self.y * other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x * other[0], self.y * other[1])
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __imul__(self, other):
        if isinstance(other, Position) or isinstance(other, Direction):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int):
            self.x *= other
            self.y *= other
        elif isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            self.x *= other[0]
            self.y *= other[1]
        else:
            raise TypeError(f"{other} is no Position, int, or tuple[int, int]")
        return self

    def __floordiv__(self, other):
        if isinstance(other, Position):
            return Position(self.x // other.x, self.y // other.y)
        if isinstance(other, int):
            return Position(self.x // other, self.y // other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x // other[0], self.y // other[1])
        raise TypeError(f"{other} is no Position, int, or tuple[int, int]")

    def __ifloordiv__(self, other):
        if isinstance(other, Position):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, int):
            self.x //= other
            self.y //= other
        elif isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            self.x //= other[0]
            self.y //= other[1]
        else:
            raise TypeError(f"{other} is no Position, int, or tuple[int, int]")
        return self

    def __neg__(self):
        return Position(-self.x, -self.y)

    def __hash__(self):
        return self.y * 10000000 + self.x

    def is_in_bounds(self, bounds) -> bool:
        if isinstance(bounds, Position):
            return 0 <= self.x < bounds.x and 0 <= self.y < bounds.y
        elif isinstance(bounds, list) and (isinstance(bounds[0], str) or isinstance(bounds[0], list)):
            return 0 <= self.x < len(bounds[0]) and 0 <= self.y < len(bounds)
        raise TypeError(f"{bounds} is no Position, list[list], or list[str]")

    def __str__(self):
        return f"Position({self.x}, {self.y})"

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(f"Invalid index {index}")

    def __setitem__(self, index: int, value: int):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(f"Invalid index {index}")

    def __mod__(self, other):
        if isinstance(other, Position):
            return Position(self.x % other.x, self.y % other.y)
        if isinstance(other, int):
            return Position(self.x & other, self.y & other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x & other[0], self.y & other[1])
        raise TypeError(f"{other} is no Position, int, or tuple[int, int]")

    def copy(self):
        return Position(self.x, self.y)


def position_and_direction_hash(position: Position, direction: Direction) -> int:
    return position.__hash__() * 10 + direction.__hash__()


class Area:
    field: list
    bounds: Position

    def __init__(self, field: list):
        self.field = field
        if isinstance(field[0], str):
            self.field = list(map(lambda line: list(line), field))
        self.bounds = Position(len(field[0]), len(field))

    @staticmethod
    def from_bounds_and_value(bounds: Position, value):
        return Area(create_2d_list(bounds.x, bounds.y, value))

    def __getitem__(self, position: Position):
        return self.field[position.y][position.x]

    def __setitem__(self, position: Position, value):
        self.field[position.y][position.x] = value

    def safe_check(self, position: Position, value):
        return position.is_in_bounds(self.bounds) and self[position] == value

    def __iter__(self):
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                yield Position(x, y)

    def is_in_bounds(self, position: Position) -> bool:
        return position.is_in_bounds(self.bounds)

    def __str__(self):
        if isinstance(self.field[0][0], Enum):
            return "\n".join(map(lambda line: "".join(map(lambda x: x.value, line)), self.field))
        else:
            return "\n".join(map(lambda line: "".join(line), self.field))

    def count(self, value) -> int:
        return sum(map(lambda line: sum([1 if x == value else 0 for x in line]), self.field))

    def flood_fill(self, start: Position, value):
        old_value = self[start]
        if old_value == value:
            return

        fields_to_fill = set()
        fields_to_fill.add(start)
        while fields_to_fill:
            position = fields_to_fill.pop()
            self[position] = value
            if self.safe_check(position + Direction.North, old_value):
                fields_to_fill.add(position + Direction.North)
            if self.safe_check(position + Direction.East, old_value):
                fields_to_fill.add(position + Direction.East)
            if self.safe_check(position + Direction.South, old_value):
                fields_to_fill.add(position + Direction.South)
            if self.safe_check(position + Direction.West, old_value):
                fields_to_fill.add(position + Direction.West)

    def get_value_set(self) -> set:
        result = set()
        for position in self:
            result.add(self[position])
        return result

    def find_first(self, value) -> Position:
        for position in self:
            if self[position] == value:
                return position
