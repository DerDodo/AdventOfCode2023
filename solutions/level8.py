from math import lcm

from util.file_util import read_input_file_id


class Map:
    nodes: dict[str, dict[str, str]]
    directions: str

    def __init__(self, lines: list[str]):
        self.nodes = {}
        self.directions = lines[0]
        for line in lines[2:]:
            node_id = line[0:3]
            left = line[7:10]
            right = line[12:15]
            self.nodes[node_id] = {"L": left, "R": right}

    def walk(self, start: str, step_id: int) -> str:
        direction = self.directions[step_id % len(self.directions)]
        return self.nodes[start][direction]


def level8_1(file_id: int) -> int:
    node_map = parse_input_file(file_id)
    position = "AAA"

    for i in range(0, 1000000000):
        position = node_map.walk(position, i)
        if position == "ZZZ":
            return i + 1
    return -1


def level8_2(file_id: int) -> int:
    node_map = parse_input_file(file_id)
    positions = list(filter(lambda node: node[-1] == "A", node_map.nodes.keys()))
    z_cycles = list(map(lambda position: walk_ghost_until_z(node_map, position), positions))
    return lcm(*z_cycles)


def walk_ghost_until_z(node_map: Map, start: str) -> int:
    position = start
    for i in range(0, 1000000000):
        position = node_map.walk(position, i)
        if position.endswith("Z"):
            return i + 1
    return -1


def parse_input_file(file_id: int) -> Map:
    lines = read_input_file_id(8, file_id)
    return Map(lines)


if __name__ == '__main__':
    print("Human steps: " + str(level8_1(3)))
    print("Ghost steps: " + str(level8_2(3)))


def test_level8():
    assert 2 == level8_1(0)
    assert 6 == level8_1(1)
    assert 6 == level8_2(2)
