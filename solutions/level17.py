import queue
from collections.abc import Sequence

from util.data_util import convert_string_list, create_2d_list
from util.file_util import read_input_file
from util.math_util import Area, Direction, Position
from util.run_util import RunTimer


class Path:
    x: int
    y: int
    score: int
    direction: Direction
    hash_value: int

    def __init__(self, x: int, y: int, score: int, direction: Direction):
        self.x = x
        self.y = y
        self.score = score
        self.direction = direction
        self.hash_value = (y * 200 + x) * 10 + direction.hash_value

    def __lt__(self, other) -> bool:
        return self.score < other.score

    def __hash__(self) -> int:
        return self.hash_value


class City(Area):
    start: Position
    end: Position
    min_field: Area

    def __init__(self, lines: list[str]):
        super().__init__(convert_string_list(lines, int))
        self.start = Position(0, 0)
        self.end = Position(self.bounds.x - 1, self.bounds.y - 1)
        self.min_field = Area(create_2d_list(self.bounds.x, self.bounds.y, 10000))

    def a_star(self, possible_steps: Sequence) -> int:
        paths_to_follow = queue.PriorityQueue()
        paths_to_follow.put(Path(self.start.x, self.start.y, 0, Direction.East))
        paths_to_follow.put(Path(self.start.x, self.start.y, 0, Direction.South))
        seen = set()

        while not paths_to_follow.empty():
            step = paths_to_follow.get()
            if step.hash_value not in seen:
                seen.add(step.hash_value)

                if step.x == self.end.x and step.y == self.end.y:
                    return step.score

                next_steps = self._a_star_calc_next_steps(step, possible_steps)
                for next_step in next_steps:
                    paths_to_follow.put(next_step)

        raise ValueError("Couldn't find end")

    def _a_star_calc_next_steps(self, path: Path, possible_steps: Sequence) -> set[Path]:
        next_steps = set()
        directions = [path.direction.turn_right_90(), path.direction.turn_left_90()]
        for direction in directions:
            new_score = path.score
            for distance in range(1, possible_steps[0]):
                new_x = path.x + direction.x * distance
                new_y = path.y + direction.y * distance

                if 0 <= new_x < self.bounds.x and 0 <= new_y < self.bounds.y:
                    new_score += self.field[path.y + direction.y * distance][path.x + direction.x * distance]

            for distance in possible_steps:
                new_x = path.x + direction.x * distance
                new_y = path.y + direction.y * distance

                if 0 <= new_x < self.bounds.x and 0 <= new_y < self.bounds.y:
                    new_score += self.field[path.y + direction.y * distance][path.x + direction.x * distance]
                    next_steps.add(Path(new_x, new_y, new_score, direction))
                else:
                    break
        return next_steps


def level17(possible_steps: Sequence) -> int:
    city = parse_input_file()
    min_heat_loss = city.a_star(possible_steps)
    return min_heat_loss


def parse_input_file() -> City:
    return City(read_input_file(17))


if __name__ == '__main__':
    timer = RunTimer()
    print("Min heat loss (1-3): " + str(level17(range(1, 4))))
    print("Min heat loss (4-10): " + str(level17(range(4, 11))))
    timer.print()


def test_level17():
    assert level17(range(1, 4)) == 102
    assert level17(range(4, 11)) == 94
