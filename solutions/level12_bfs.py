from copy import deepcopy

from solutions.level12_dfs import State
from solutions.level12_naive import parse_input_file, is_still_possible


class Possibility:
    num_arrangements: int
    arrangement: str
    covered_groups: list[int]
    remaining_groups: list[int]
    group_i: int

    def __init__(self, num_arrangements: int, arrangement: str, covered_groups: list[int], remaining_groups: list[int],
                 group_i: int):
        self.num_arrangements = num_arrangements
        self.arrangement = arrangement
        self.covered_groups = covered_groups
        self.remaining_groups = remaining_groups
        self.group_i = group_i


def level12_bfs(unfold: bool) -> int:
    rows = parse_input_file(unfold)
    return sum(map(lambda row: get_num_arrangements(row[0], row[1]), rows))


def get_num_arrangements(row: str, definition: list[int]) -> int:
    possible_arrangements = generate_all_possible_arrangements(row, definition)
    sum_arrangements = sum(
        map(lambda a: a.num_arrangements,
            filter(lambda a: is_correct_arrangement(a.arrangement, definition), possible_arrangements)))
    return sum_arrangements


def generate_all_possible_arrangements(arrangement: str, definition: list[int]) -> list[Possibility]:
    unknowns = list(map(lambda char: char[0], filter(lambda char: char[1] == "?", enumerate(list(arrangement)))))
    possibilities = [Possibility(1, arrangement, [], deepcopy(definition), 0)]
    for i in range(0, len(arrangement)):
        if arrangement[i] == "?":
            new_possibilities = []
            for possibility in possibilities:
                dot_version = possibility.arrangement[:i] + "." + possibility.arrangement[i + 1:]
                if is_still_possible(dot_version, unknowns, definition):
                    new_possibility = deepcopy(possibility)
                    new_possibility.arrangement = dot_version
                    if new_possibility.group_i > 0:
                        new_possibility.group_i = 0
                        new_possibility.covered_groups.append(new_possibility.remaining_groups.pop(0))
                    new_possibilities.append(new_possibility)

                hash_version = possibility.arrangement[:i] + "#" + possibility.arrangement[i + 1:]
                if is_still_possible(hash_version, unknowns, definition):
                    new_possibility = deepcopy(possibility)
                    new_possibility.arrangement = hash_version
                    new_possibility.group_i += 1
                    new_possibilities.append(new_possibility)

            unified_possibilities = []
            already_unified = []
            for j, possibility in enumerate(new_possibilities):
                if j in already_unified:
                    continue

                for k, other_possibility in enumerate(new_possibilities[j + 1:]):
                    if j + k + 1 in already_unified:
                        continue

                    if (possibility.arrangement[i] == other_possibility.arrangement[i] and
                            possibility.covered_groups == other_possibility.covered_groups and
                            possibility.group_i == other_possibility.group_i
                    ):
                        possibility.num_arrangements += other_possibility.num_arrangements
                        already_unified.append(j + k + 1)

                unified_possibilities.append(possibility)
            possibilities = unified_possibilities
        elif arrangement[i] == ".":
            for possibility in possibilities:
                if possibility.group_i != 0:
                    if possibility.group_i == possibility.remaining_groups[0]:
                        possibility.group_i = 0
                        possibility.covered_groups.append(possibility.remaining_groups.pop(0))
                    else:
                        raise Exception(f"Checking an invalid configuration here!")
        elif arrangement[i] == "#":
            for possibility in possibilities:
                possibility.group_i += 1
                if not possibility.remaining_groups or possibility.group_i > possibility.remaining_groups[0]:
                    raise Exception(f"Checking an invalid configuration here!")
        i += 1
    return possibilities


def go_to_next_question_mark(arrangement: str, definition: list[int], i: int, group_i: int, next_group: int) -> tuple[
    int, int, int, str, State]:
    while i < len(arrangement):
        if arrangement[i] == "#":
            group_i += 1
            if next_group >= len(definition) or group_i > definition[next_group]:
                return i, group_i, next_group, arrangement, State.WRONG_CONFIGURATION
        elif arrangement[i] == ".":
            if group_i != 0:
                if group_i == definition[next_group]:
                    next_group += 1
                    group_i = 0
                else:
                    return i, group_i, next_group, arrangement, State.WRONG_CONFIGURATION
        else:
            break
        i += 1
    return i, group_i, next_group, arrangement, State.END if i == len(arrangement) else State.CONTINUE


def fill_started_group(arrangement: str, definition: list[int], i: int, group_i: int, next_group: int) -> tuple[
    int, int, int, str, State]:
    if group_i > 0 or arrangement[i] == "#":
        checked_part = arrangement[:i]
        # check if next group can still be filled
        if next_group >= len(definition):
            return i, group_i, next_group, checked_part, State.WRONG_CONFIGURATION
        remaining_group_length = definition[next_group] - group_i
        if i + remaining_group_length > len(arrangement):
            return i, group_i, next_group, checked_part, State.WRONG_CONFIGURATION
        for j in range(0, remaining_group_length):
            if arrangement[i + j] != "#" and arrangement[i + j] != "?":
                return i, group_i, next_group, checked_part, State.WRONG_CONFIGURATION
        i += remaining_group_length
        checked_part = checked_part + "#" * remaining_group_length
        # check if block ends correctly
        if i == len(arrangement):
            return i, group_i, next_group, checked_part + arrangement[i:], State.END
        if arrangement[i] == "#":
            return i, group_i, next_group, checked_part + arrangement[i:], State.WRONG_CONFIGURATION
        elif arrangement[i] == "?":
            checked_part = checked_part + "."
            i += 1
        return i, 0, next_group + 1, checked_part + arrangement[i:], State.END if i == len(
            arrangement) else State.CONTINUE
    return i, 0, next_group, arrangement, State.END if i == len(arrangement) else State.CONTINUE


def is_correct_arrangement(arrangement: str, definition: list[int]) -> bool:
    return get_spring_list(arrangement) == definition


def get_spring_list(arrangement: str) -> list[int]:
    spring_list = []
    spring_count = 0
    for char in arrangement:
        if char == "#":
            spring_count += 1
        if char == "." and spring_count > 0:
            spring_list.append(spring_count)
            spring_count = 0
    if spring_count > 0:
        spring_list.append(spring_count)
    return spring_list


if __name__ == '__main__':
    print("Sum possible arrangements (folded): " + str(level12_bfs(False)))
    print("Sum possible arrangements (unfolded): " + str(level12_bfs(True)))


def test_level12():
    assert 21 == level12_bfs(False)
    assert 525152 == level12_bfs(True)
