import random
from copy import deepcopy
from enum import Enum

from util.file_util import read_input_file


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def remove_direction(directions: list[Direction], direction: Direction):
    if direction in directions:
        directions.remove(direction)


class Path:
    field: list[list[int]]
    x: int
    y: int
    heat_loss: int
    history: list[Direction]

    def __init__(self, field: list[list[int]], x: int, y: int, heat_loss: int, last_steps: list[Direction]):
        self.field = field
        self.x = x
        self.y = y
        self.heat_loss = heat_loss
        self.history = last_steps

    def get_random_next_step(self) -> Direction:
        directions = list(Direction)
        if len(self.history) >= 3 and self.history[-1] == self.history[-2] == self.history[-3]:
            if self.history[-1] == Direction.UP or self.history[-1] == Direction.DOWN:
                directions = [Direction.LEFT, Direction.RIGHT]
            else:
                directions = [Direction.UP, Direction.DOWN]

        if self.x == 0:
            remove_direction(directions, Direction.LEFT)
        if self.y == 0:
            remove_direction(directions, Direction.UP)
        if self.x == len(self.field[0]) - 1:
            remove_direction(directions, Direction.RIGHT)
        if self.y == len(self.field) - 1:
            remove_direction(directions, Direction.DOWN)

        if len(self.history) > 0:
            if self.history[-1] == Direction.LEFT:
                remove_direction(directions, Direction.RIGHT)
            if self.history[-1] == Direction.RIGHT:
                remove_direction(directions, Direction.LEFT)
            if self.history[-1] == Direction.UP:
                remove_direction(directions, Direction.DOWN)
            if self.history[-1] == Direction.DOWN:
                remove_direction(directions, Direction.UP)

        if Direction.RIGHT in directions:
            directions.append(Direction.RIGHT)
            directions.append(Direction.RIGHT)
            directions.append(Direction.RIGHT)
        if Direction.DOWN in directions:
            directions.append(Direction.DOWN)
            directions.append(Direction.DOWN)
            directions.append(Direction.DOWN)

        return random.choice(directions)

    def step(self, direction: Direction):
        if direction == Direction.UP:
            self.y -= 1
        elif direction == Direction.LEFT:
            self.x -= 1
        elif direction == Direction.DOWN:
            self.y += 1
        else:
            self.x += 1
        self.heat_loss += self.field[self.y][self.x]
        self.history.append(direction)

    def get_distance_to_exit(self) -> int:
        return (len(self.field[0]) - self.x - 1) + (len(self.field) - self.y - 1)

    def is_done(self) -> bool:
        return self.x == len(self.field[0]) - 1 and self.y == len(self.field) - 1


def generate_new_initial_path(field: list[list[int]], path: Path, length: int):
    new_path = Path(field, 0, 0, 0, list())
    for i in range(0, length):
        new_path.step(path.history[i])
    return new_path


def level17() -> int:
    field = parse_input_file()
    min_heat_loss = 10000000000000000000
    since_last_best = 0
    initial_path = Path(field, 0, 0, 0, list())
    for i in range(0, 1000):
        print(f"Attempt {i}...")
        min_heat_loss_attempt = level17_attempt(field, initial_path)
        since_last_best += 1
        if min_heat_loss_attempt.heat_loss < min_heat_loss:
            min_heat_loss = min_heat_loss_attempt.heat_loss
            since_last_best = 0
            print(f"Min heat loss: {min_heat_loss}")
        if since_last_best > 150:
            print("Aborting")
            break
    return min_heat_loss


def level17_attempt(field, initial_path: Path) -> Path:
    paths = [initial_path]

    min_heat_loss = 10000000000000000000
    min_heat_loss_path = None
    found_paths = 0
    for _ in range(0, len(field)):
        new_paths = []
        for path in paths:
            new_paths.extend(attempt_path_multiple_times(path))

        done_paths = list(filter(lambda p: p.is_done(), new_paths))
        if len(done_paths) != 0:
            found_paths += len(done_paths)
            new_best_heat_loss = min(map(lambda p: p.heat_loss, done_paths))
            if new_best_heat_loss < min_heat_loss:
                min_heat_loss = new_best_heat_loss
                min_heat_loss_path = list(filter(lambda p: p.heat_loss == min_heat_loss, done_paths))[0]
            if found_paths > len(field) * len(field[0]):
                break
        if len(done_paths) == len(new_paths):
            break

        not_done_paths = list(filter(lambda p: not p.is_done(), new_paths))

        chosen_paths = []
        chosen_paths.extend(choose_best_paths(not_done_paths, lambda p: p.heat_loss))
        chosen_paths.extend(choose_best_paths(not_done_paths, lambda p: p.get_distance_to_exit()))

        paths = chosen_paths

    return min_heat_loss_path


def parse_input_file() -> list[list[int]]:
    lines = read_input_file(17)
    return list(map(lambda line: list(map(int, list(line))), lines))


def attempt_path_multiple_times(path: Path) -> list[Path]:
    paths = []
    if path.is_done():
        return [path]

    for _ in range(0, 50):
        new_path = deepcopy(path)
        for _ in range(0, int((len(path.field[0]) + len(path.field)) / 2)):
            direction = new_path.get_random_next_step()
            new_path.step(direction)
            if new_path.is_done():
                break
        paths.append(new_path)

    return paths


def choose_best_paths(paths: list[Path], sort_mechanism) -> list[Path]:
    paths.sort(key=sort_mechanism)
    chosen_paths = []
    for path in paths:
        already_chosen = False
        for chosen_path in chosen_paths:
            if path.x == chosen_path.x and path.y == chosen_path.y and path.heat_loss == chosen_path.heat_loss and path.history == chosen_path.history:
                already_chosen = True

        if not already_chosen:
            chosen_paths.append(path)
            if len(chosen_paths) == 4:
                return chosen_paths
    return chosen_paths


if __name__ == '__main__':
    print("Final minimal heat loss: " + str(level17()))


def test_level17():
    assert 102 == level17()
