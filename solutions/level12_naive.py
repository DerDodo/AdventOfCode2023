from enum import Enum

from util.file_util import read_input_file


def level12_naive(unfold: bool) -> int:
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
    possible_arrangements = generate_all_possible_arrangements(row, unknowns, definition)
    sum_arrangements = sum(is_correct_arrangement(arrangement, definition) for arrangement in possible_arrangements)
    print(f"{sum_arrangements} for {row}")
    return sum_arrangements


def generate_all_possible_arrangements(arrangement: str, unknowns: list[int], definition: list[int]) -> list[str]:
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
            possible_arrangements.extend(generate_all_possible_arrangements(new_arrangement, unknowns[1:], definition))

    if arrangement.count("#") < sum(definition):
        new_arrangement = arrangement[:unknowns[0]] + "#" + arrangement[unknowns[0] + 1:]
        if is_still_possible(new_arrangement, unknowns, definition):
            possible_arrangements.extend(generate_all_possible_arrangements(new_arrangement, unknowns[1:], definition))

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
            if next_group >= len(definition) or group_i > definition[next_group]:
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
    print("Sum possible arrangements (folded): " + str(level12_naive(False)))
    print("Sum possible arrangements (unfolded): " + str(level12_naive(True)))


def test_level12():
    assert 21 == level12_naive(False)
    assert 525152 == level12_naive(True)
