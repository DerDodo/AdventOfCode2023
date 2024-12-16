from util.data_util import transpose
from util.file_util import read_input_file


def level13(with_smudge: bool) -> int:
    fields = parse_input_file()
    total_sum = 0
    i = 0
    for field in fields:
        rows = get_num_reflected_rows(field, with_smudge)
        cols = get_num_reflected_rows(transpose(field), with_smudge)
        total_sum += rows * 100 + cols
        i += 1

    return total_sum


def parse_input_file() -> list[list[list[str]]]:
    lines = read_input_file(13)
    areas = []
    next_area = []
    for line in lines:
        if line == "":
            areas.append(next_area)
            next_area = []
        else:
            next_area.append(list(line))

    if next_area:
        areas.append(next_area)

    return areas


def get_num_reflected_rows(field: list[list[str]], with_smudge: bool) -> int:
    reflection_lines: list[tuple[int, bool]] = []
    for reflection_line in range(0, len(field) - 1):
        equal, smudge_available = are_rows_equal(field[reflection_line], field[reflection_line + 1], with_smudge)
        if equal:
            reflection_lines.append((reflection_line + 1, smudge_available))

    if not reflection_lines:
        return 0

    for reflection_line in reflection_lines:
        smudge_available = reflection_line[1]
        check_distance = 1
        correct = True
        while reflection_line[0] + check_distance < len(field) and reflection_line[0] - check_distance - 1 >= 0:
            equal, smudge_available = are_rows_equal(
                field[reflection_line[0] + check_distance],
                field[reflection_line[0] - check_distance - 1],
                smudge_available)
            if not equal:
                correct = False
                break
            check_distance += 1

        if correct and not smudge_available:
            return reflection_line[0]

    return 0


def are_rows_equal(row1: list[str], row2: list[str], smudge_available: bool) -> tuple[bool, bool]:
    one_off_available = smudge_available
    for i in range(0, len(row1)):
        if row1[i] != row2[i]:
            if one_off_available:
                one_off_available = False
            else:
                return False, smudge_available
    return True, one_off_available


if __name__ == '__main__':
    print("Reflection value (no smudge): " + str(level13(False)))
    print("Reflection value (with smudge): " + str(level13(True)))


def test_level13():
    assert 405 == level13(False)
    assert 400 == level13(True)
