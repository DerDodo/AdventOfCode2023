from enum import Enum

from solutions.level12_naive import parse_input_file, is_correct_arrangement
from util.file_util import read_input_file


class State(Enum):
    CONTINUE = 0
    WRONG_CONFIGURATION = 1
    END = 2


def level12_dfs(unfold: bool) -> int:
    rows = parse_input_file(unfold)
    return sum(map(lambda row: get_num_arrangements(row[0], row[1]), rows))


def get_num_arrangements(row: str, definition: list[int]) -> int:
    possible_arrangements = generate_all_possible_arrangements(row, definition, 0, 0, 0)
    sum_arrangements = sum(is_correct_arrangement(arrangement, definition) for arrangement in possible_arrangements)
    print(f"{sum_arrangements} for {row}")
    return sum_arrangements


def generate_all_possible_arrangements(arrangement: str, definition: list[int], i: int, group_i: int, next_group: int) -> list[str]:
    search_and_fill = True
    current_arrangement = arrangement
    while search_and_fill:
        search_and_fill = False
        i, group_i, next_group, current_arrangement, state = go_to_next_question_mark(current_arrangement, definition, i, group_i, next_group)
        if state == State.END:
            return [current_arrangement]
        elif state == State.WRONG_CONFIGURATION:
            return []

        while group_i > 0 or current_arrangement[i] == "#":
            search_and_fill = True
            i, group_i, next_group, current_arrangement, state = fill_started_group(current_arrangement, definition, i, group_i, next_group)
            if state == State.END:
                return [current_arrangement]
            elif state == State.WRONG_CONFIGURATION:
                return []

    dot_version = current_arrangement[:i] + "." + current_arrangement[i+1:]
    versions = generate_all_possible_arrangements(dot_version, definition, i + 1, 0, next_group)
    if next_group < len(definition):
        hash_version = current_arrangement[:i] + "#" + current_arrangement[i+1:]
        hash_versions = generate_all_possible_arrangements(hash_version, definition, i + 1, group_i + 1, next_group)
        versions.extend(hash_versions)
    return list(filter(lambda a: a.count("#") == sum(definition), versions))


def go_to_next_question_mark(arrangement: str, definition: list[int], i: int, group_i: int, next_group: int) -> tuple[int, int, int, str, State]:
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


def fill_started_group(arrangement: str, definition: list[int], i: int, group_i: int, next_group: int) -> tuple[int, int, int, str, State]:
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
        return i, 0, next_group + 1, checked_part + arrangement[i:], State.END if i == len(arrangement) else State.CONTINUE
    return i, 0, next_group, arrangement, State.END if i == len(arrangement) else State.CONTINUE


if __name__ == '__main__':
    print("Sum possible arrangements (folded): " + str(level12_dfs(False)))
    print("Sum possible arrangements (unfolded): " + str(level12_dfs(True)))


def test_level12():
    assert 21 == level12_dfs(False)
    assert 525152 == level12_dfs(True)
