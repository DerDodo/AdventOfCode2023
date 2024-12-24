from util.data_util import create_3d_list
from util.file_util import read_input_file
from util.math_util import clamp
from util.run_util import RunTimer


class Brick:
    start_x: int
    start_y: int
    start_z: int
    end_x: int
    end_y: int
    end_z: int

    def __init__(self, line: str):
        parts = line.split("~")
        self.start_x, self.start_y, self.start_z = map(int, parts[0].split(","))
        self.end_x, self.end_y, self.end_z = map(int, parts[1].split(","))

    def get_delta(self) -> tuple[int, int, int]:
        return clamp(self.end_x - self.start_x), clamp(self.end_y - self.start_y), clamp(self.end_z - self.start_z)

    def __iter__(self) -> tuple[int, int, int]:
        position_x, position_y, position_z = self.start_x, self.start_y, self.start_z
        delta_x, delta_y, delta_z = self.get_delta()

        while position_x != self.end_x or position_y != self.end_y or position_z != self.end_z:
            yield position_x, position_y, position_z
            position_x += delta_x
            position_y += delta_y
            position_z += delta_z

        yield position_x, position_y, position_z


class Area:
    bricks: list[Brick]
    field: list[list[list[bool]]]

    def __init__(self, bricks: list[Brick]):
        self.bricks = bricks
        self._init_field()

    def _init_field(self):
        max_x, max_y, max_z = self.bricks[0].start_x, self.bricks[0].start_y, self.bricks[0].start_z

        for brick in self.bricks:
            max_x = max(max_x, brick.start_x, brick.end_x)
            max_y = max(max_y, brick.start_y, brick.end_y)
            max_z = max(max_z, brick.start_z, brick.end_z)

        self.field = create_3d_list(max_x + 1, max_y + 1, max_z + 1, False)

        for x in range(max_x + 1):
            for y in range(max_y + 1):
                self.field[x][y][0] = True

        for brick in self.bricks:
            self.add_brick(brick)

    def let_bricks_fall(self):
        unstable_bricks = []
        for brick in self.bricks:
            unstable_bricks.append(brick)
        unstable_bricks.sort(key=lambda b: min(b.start_z, b.end_z))

        while unstable_bricks:
            i = 0
            while i < len(unstable_bricks):
                brick = unstable_bricks[i]
                if self.can_brick_move(brick):
                    self.move_brick(brick)
                    i += 1
                else:
                    unstable_bricks.pop(i)

        self.bricks.sort(key=lambda b: min(b.start_z, b.end_z))

    def can_brick_move(self, brick: Brick) -> bool:
        if brick.start_z == brick.end_z:
            for position_x, position_y, position_z in brick:
                if self.field[position_x][position_y][position_z - 1]:
                    return False
            return True
        else:
            z_check = min(brick.start_z, brick.end_z) - 1
            return not self.field[brick.start_x][brick.start_y][z_check]

    def move_brick(self, brick: Brick):
        self.remove_brick(brick)

        brick.start_z -= 1
        brick.end_z -= 1

        self.add_brick(brick)

    def remove_brick(self, brick: Brick):
        for position_x, position_y, position_z in brick:
            self.field[position_x][position_y][position_z] = False

    def add_brick(self, brick: Brick):
        for position_x, position_y, position_z in brick:
            self.field[position_x][position_y][position_z] = True

    def calc_disintegration(self) -> tuple[int, int]:
        num_stable_bricks = 0
        num_chain_reactions = 0
        for brick_i in range(len(self.bricks)):
            brick = self.bricks[brick_i]
            removed_bricks: set[int] = {brick_i}
            self.remove_brick(brick)

            for other_brick_i in range(brick_i + 1, len(self.bricks), 1):
                other_brick = self.bricks[other_brick_i]
                if other_brick_i not in removed_bricks and self.can_brick_move(other_brick):
                    removed_bricks.add(other_brick_i)
                    self.remove_brick(other_brick)

            if len(removed_bricks) == 1:
                num_stable_bricks += 1
            num_chain_reactions += len(removed_bricks) - 1

            for removed_brick_i in removed_bricks:
                self.add_brick(self.bricks[removed_brick_i])

        return num_stable_bricks, num_chain_reactions


def parse_input_file() -> Area:
    lines = read_input_file(22)
    bricks = list(map(Brick, lines))
    return Area(bricks)


def level22() -> tuple[int, int]:
    area = parse_input_file()
    area.let_bricks_fall()
    return area.calc_disintegration()


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num disintegratable bricks: {level22()}")
    timer.print()


def test_level21():
    assert level22() == (5, 7)
