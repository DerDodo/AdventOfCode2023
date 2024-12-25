import math

from util.file_util import read_input_file
from util.run_util import RunTimer


class Hailstone:
    p_x: int
    p_y: int
    p_z: int
    v_x: int
    v_y: int
    v_z: int

    k: float
    d: float

    def __init__(self, line: str):
        parts = line.replace(",", "").replace("  ", " ").split(" ")
        self.p_x = int(parts[0])
        self.p_y = int(parts[1])
        self.p_z = int(parts[2])
        self.v_x = int(parts[4])
        self.v_y = int(parts[5])
        self.v_z = int(parts[6])

        self.k = self.v_y / self.v_x
        self.d = int(self.p_y - self.k * self.p_x)

    def intersects(self, other, area_min: int, area_max: int) -> bool:
        if math.isclose(self.k, other.k):
            return False

        x = (other.d - self.d) / (self.k - other.k)
        y = self.k * x + self.d

        if (self.v_x > 0 and x < self.p_x) or (self.v_x < 0 and x > self.p_x) or (other.v_x > 0 and x < other.p_x) or (other.v_x < 0 and x > other.p_x):
            return False

        return area_min <= x <= area_max and area_min <= y <= area_max


def parse_input_file() -> list[Hailstone]:
    lines = read_input_file(24)
    return list(map(Hailstone, lines))


def level24_1(area_min: int, area_max: int) -> int:
    hailstones = parse_input_file()
    num_intersections = 0
    for a in range(len(hailstones) - 1):
        for b in range(a + 1, len(hailstones)):
            if hailstones[a].intersects(hailstones[b], area_min, area_max):
                num_intersections += 1
    return num_intersections


def level24_2() -> int:
    return 0


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num hailstones: {level24_1(200000000000000, 400000000000000)}")
    print(f"Position id for stone throw: {level24_2()}")
    timer.print()


def test_level21():
    assert level24_1(7, 27) == 2
    assert level24_2() == 47
