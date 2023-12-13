from enum import Enum

from util.file_util import read_input_file


class State(Enum):
    CONTINUE = 0
    WRONG_CONFIGURATION = 1
    END = 2


def level12(unfold: bool) -> int:
    rows = parse_input_file(unfold)
    return sum(map(lambda row: get_num_arrangements(row[0], row[1]), rows))


def parse_input_file(unfold: bool) -> list[tuple[str, list[int]]]:
    lines = read_input_file(12)
    plans = list(map(split_input_line, lines))
    if unfold:
        return list(map(lambda plan: (plan[0] + ("?" + plan[0]) * 4, plan[1] * 5), plans))
    else:
        return plans


def split_input_line(row: str) -> tuple[str, list[int]]:
    parts = row.split(" ")
    return parts[0], list(map(int, parts[1].split(",")))


def get_num_arrangements(row: str, definition: list[int]) -> int:
    unknowns = list(map(lambda char: char[0], filter(lambda char: char[1] == "?", enumerate(list(row)))))
    #possible_arrangements_old = generate_all_possible_arrangements1(row, unknowns, definition)
    possible_arrangements = generate_all_possible_arrangements2(row, definition, 0, 0, 0)
    #sum_arrangements_old = sum(is_correct_arrangement(arrangement, definition) for arrangement in possible_arrangements_old)
    sum_arrangements = sum(is_correct_arrangement(arrangement, definition) for arrangement in possible_arrangements)
    print(f"{sum_arrangements} for {row}")
    return sum_arrangements


def generate_all_possible_arrangements2(arrangement: str, definition: list[int], i: int, group_i: int, next_group: int) -> list[str]:
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
    versions = generate_all_possible_arrangements2(dot_version, definition, i + 1, 0, next_group)
    if next_group < len(definition):
        hash_version = current_arrangement[:i] + "#" + current_arrangement[i+1:]
        hash_versions = generate_all_possible_arrangements2(hash_version, definition, i + 1, group_i + 1, next_group)
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


def generate_all_possible_arrangements1(arrangement: str, unknowns: list[int], definition: list[int]) -> list[str]:
    if len(unknowns) == 0:
        return [arrangement]

    if arrangement.count("#") == sum(definition):
        only_arrangement = arrangement.replace("?", ".")
        if is_correct_arrangement(only_arrangement, definition):
            return [only_arrangement]
    elif arrangement.count("#") + arrangement.count("?") == sum(definition):
        only_arrangement = arrangement.replace("?", "#")
        if is_correct_arrangement(only_arrangement, definition):
            return [only_arrangement]

    possible_arrangements = []

    if sum(unknowns) > sum(definition) - arrangement.count("#"):
        new_arrangement = arrangement[:unknowns[0]] + "." + arrangement[unknowns[0] + 1:]
        if is_still_possible(new_arrangement, unknowns, definition):
            possible_arrangements.extend(generate_all_possible_arrangements1(new_arrangement, unknowns[1:], definition))

    if arrangement.count("#") < sum(definition):
        new_arrangement = arrangement[:unknowns[0]] + "#" + arrangement[unknowns[0] + 1:]
        if is_still_possible(new_arrangement, unknowns, definition):
            possible_arrangements.extend(generate_all_possible_arrangements1(new_arrangement, unknowns[1:], definition))

    return possible_arrangements


def is_still_possible(arrangement: str, unknowns: list[int], definition: list[int]) -> bool:
    found_unknown = arrangement.find("?")
    if found_unknown == -1:
        return is_correct_arrangement(arrangement, definition)

    if arrangement.count("#") < sum(definition) - len(unknowns):
        return False

    next_group = 0
    group_i = 0
    i = 0
    # find group before ?
    while i < len(arrangement):
        if arrangement[i] == "#":
            group_i += 1
            if group_i > definition[next_group]:
                return False
        elif arrangement[i] == ".":
            if group_i != 0:
                if group_i == definition[next_group]:
                    next_group += 1
                    group_i = 0
                else:
                    return False
        else:
            break
        i += 1
    if group_i > 0:
        # check if next group can still be filled
        for _ in range(0, definition[next_group] - group_i):
            if i >= len(arrangement) or (arrangement[i] != "#" and arrangement[i] != "?"):
                return False
            i += 1
        # check if block ends correctly
        if i != len(arrangement) and arrangement[i] == "#":
            return False
    return True


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
    print("Sum possible arrangements (folded): " + str(level12(False)))
    print("Sum possible arrangements (unfolded): " + str(level12(True)))


def test_level12():
    assert 21 == level12(False)
    assert 525152 == level12(True)
