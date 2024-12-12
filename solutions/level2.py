from enum import Enum
from typing import Tuple

from util.file_util import read_input_file, read_input_file


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Game:
    game_id: int
    draws: list[dict[Color, int]]

    def __init__(self, line: str):
        parts = line.split(":")
        self.draws = list()
        self.game_id = int(parts[0][5:])
        draws = parts[1].split(";")
        for draw in draws:
            cubes = draw.split(",")
            new_draw = dict()
            for cube_color in cubes:
                definition = cube_color.strip().split(" ")
                new_draw[Color(definition[1])] = int(definition[0])
            self.draws.append(new_draw)

    def has_max(self, red: int, green: int, blue: int) -> False:
        for draw in self.draws:
            for cubes in draw.items():
                if ((cubes[0] == Color.RED and cubes[1] > red) or
                        (cubes[0] == Color.GREEN and cubes[1] > green) or
                        (cubes[0] == Color.BLUE and cubes[1] > blue)):
                    return False
        return True

    def get_max_cubes(self) -> dict[Color, int]:
        max_cubes = {
            Color.RED: 0,
            Color.GREEN: 0,
            Color.BLUE: 0,
        }
        for draw in self.draws:
            for cubes in draw.items():
                max_cubes[cubes[0]] = max(cubes[1], max_cubes[cubes[0]])
        return max_cubes


def parse_input_file() -> list[Game]:
    return list(map(Game, read_input_file(2)))


def level2() -> Tuple[int, int]:
    games = parse_input_file()
    sum_games = 0
    power_games = 0
    for game in games:
        if game.has_max(12, 13, 14):
            sum_games += game.game_id
        max_cubes = game.get_max_cubes()
        power_games += max_cubes[Color.RED] * max_cubes[Color.GREEN] * max_cubes[Color.BLUE]
    return sum_games, power_games


if __name__ == '__main__':
    print("Game result: " + str(level2()))


def test_level1():
    assert (8, 2286) == level2()
