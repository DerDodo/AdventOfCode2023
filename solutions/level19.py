from enum import Enum

from util.data_util import split_input_when_empty
from util.file_util import read_input_file
from util.run_util import RunTimer


class Condition(Enum):
    GreaterThan = ">"
    SmallerThan = "<"
    PassThrough = "-"

    def evaluate(self, left: int, right: int) -> bool:
        match self:
            case Condition.GreaterThan:
                return left > right
            case Condition.SmallerThan:
                return left < right
            case Condition.PassThrough:
                return True


class Part:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, line: str):
        parts = line[1:-1].split(",")
        self.x = int(parts[0][2:])
        self.m = int(parts[1][2:])
        self.a = int(parts[2][2:])
        self.s = int(parts[3][2:])

    def __str__(self):
        return f"x={{{self.x},m={self.m},a={self.a},s={self.s}}}"

    def get_rating(self) -> int:
        return self.x + self.m + self.a + self.s

    def __getitem__(self, item) -> int:
        if item == "x":
            return self.x
        elif item == "m":
            return self.m
        elif item == "a":
            return self.a
        elif item == "s":
            return self.s
        else:
            raise ValueError(f"Invalid item: {item}")


class Action:
    variable: str | None
    condition: Condition
    value: int | None
    target: str

    def __init__(self, text: str):
        split = text.find("<")
        if split != -1:
            self.condition = Condition.SmallerThan
        else:
            split = text.find(">")
            if split != -1:
                self.condition = Condition.GreaterThan
            else:
                self.condition = Condition.PassThrough
        if split != -1:
            condition_split = text.find(":")
            self.variable = text[0:split]
            self.value = int(text[split+1:condition_split])
            self.target = text[condition_split+1:]
        else:
            self.target = text

    def __str__(self):
        if self.condition == Condition.PassThrough:
            return self.target
        else:
            return f"{self.variable}{self.condition.value}{self.value}:{self.target}"

    def fits(self, part: Part):
        if self.condition == Condition.PassThrough:
            return True
        else:
            return self.condition.evaluate(part[self.variable], self.value)


class PartsRange:
    x_start: int
    x_end: int
    m_start: int
    m_end: int
    a_start: int
    a_end: int
    s_start: int
    s_end: int

    def __init__(self):
        self.x_start = 1
        self.m_start = 1
        self.a_start = 1
        self.s_start = 1
        self.x_end = 4000
        self.m_end = 4000
        self.a_end = 4000
        self.s_end = 4000

    @staticmethod
    def create_empty():
        parts_range = PartsRange()
        parts_range.x_end = 1
        parts_range.m_end = 1
        parts_range.a_end = 1
        parts_range.s_end = 1
        return parts_range

    def copy(self):
        new_parts_range = PartsRange()
        new_parts_range.x_start = self.x_start
        new_parts_range.m_start = self.m_start
        new_parts_range.a_start = self.a_start
        new_parts_range.s_start = self.s_start
        new_parts_range.x_end = self.x_end
        new_parts_range.m_end = self.m_end
        new_parts_range.a_end = self.a_end
        new_parts_range.s_end = self.s_end
        return new_parts_range

    def calc_valid_parts(self) -> int:
        return ((self.x_end - self.x_start + 1) *
                (self.m_end - self.m_start + 1) *
                (self.a_end - self.a_start + 1) *
                (self.s_end - self.s_start + 1))

    def split(self, action: Action) -> tuple:
        if_true = self.copy()
        if_false = self.copy()
        if action.condition == Condition.SmallerThan:
            if action.variable == "x" and self.x_end > action.value:
                if_true.x_end = action.value - 1
                if_false.x_start = action.value
            elif action.variable == "m" and self.m_end > action.value:
                if_true.m_end = action.value - 1
                if_false.m_start = action.value
            elif action.variable == "a" and self.a_end > action.value:
                if_true.a_end = action.value - 1
                if_false.a_start = action.value
            elif action.variable == "s" and self.s_end > action.value:
                if_true.s_end = action.value - 1
                if_false.s_start = action.value
            else:
                if_false = self.create_empty()
        elif action.condition == Condition.GreaterThan:
            if action.variable == "x" and self.x_start < action.value:
                if_false.x_end = action.value
                if_true.x_start = action.value + 1
            elif action.variable == "m" and self.m_start < action.value:
                if_false.m_end = action.value
                if_true.m_start = action.value + 1
            elif action.variable == "a" and self.a_start < action.value:
                if_false.a_end = action.value
                if_true.a_start = action.value + 1
            elif action.variable == "s" and self.s_start < action.value:
                if_false.s_end = action.value
                if_true.s_start = action.value + 1
            else:
                if_false = self.create_empty()
        return if_true, if_false

    def is_empty(self) -> bool:
        return self.calc_valid_parts() == 0


class Workflow:
    name: str
    actions: list[Action]

    def __init__(self, line: str):
        parts = line.split("{")
        self.name = parts[0]
        actions = parts[1][:-1].split(",")
        self.actions = list(map(Action, actions))

    def __str__(self):
        actions = ",".join(map(str, self.actions))
        return f"{self.name}{{{actions}}}"

    def process(self, part: Part) -> str:
        for action in self.actions:
            if action.fits(part):
                return action.target

        raise ValueError("Invalid workflow")

    def calc_valid_configurations(self, workflows: dict, parts_range: PartsRange) -> int:
        sum_valid_parts_ranges = 0
        remaining_range = parts_range
        for action in self.actions:
            if action.condition == Condition.PassThrough:
                sum_valid_parts_ranges += self.calc_valid_configurations_for_action(workflows, remaining_range, action)
            else:
                if_true, remaining_range = remaining_range.split(action)
                sum_valid_parts_ranges += self.calc_valid_configurations_for_action(workflows, if_true, action)
                if remaining_range.is_empty():
                    break

        return sum_valid_parts_ranges

    def calc_valid_configurations_for_action(self, workflows: dict, parts_range: PartsRange, action: Action) -> int:
        if action.target == "A":
            return parts_range.calc_valid_parts()
        elif action.target != "R":
            return workflows[action.target].calc_valid_configurations(workflows, parts_range)
        else:
            return 0


def parse_input_file() -> tuple[dict[str, Workflow], list[Part]]:
    lines = read_input_file(19)
    input_parts = split_input_when_empty(lines)
    workflows = list(map(Workflow, input_parts[0]))
    workflow_dict = {w.name: w for w in workflows}
    parts = list(map(Part, input_parts[1]))
    return workflow_dict, parts


def level19() -> tuple[int, int]:
    workflows, parts = parse_input_file()
    total_rating = 0

    for part in parts:
        next_workflow = "in"
        while next_workflow != "A" and next_workflow != "R":
            next_workflow = workflows[next_workflow].process(part)
        if next_workflow == "A":
            total_rating += part.get_rating()

    parts_range = PartsRange()
    num_valid_configurations = workflows["in"].calc_valid_configurations(workflows, parts_range)

    return total_rating, num_valid_configurations


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Sum part rating: {level19()}")
    timer.print()


def test_level19():
    assert (level19()) == (19114, 167409079868000)
