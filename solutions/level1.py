from util.file_util import read_input_file_id


def process_line(line: str) -> int:
    digits = list(filter(str.isdigit, line))
    return int(digits[0]) * 10 + int(digits[-1])


def process_line_with_text(line: str) -> int:
    digits = []
    for idx, character in enumerate(line):
        if character.isdigit():
            digits.append(int(character))
        else:
            text_number = is_text_number(line, idx)
            if text_number:
                digits.append(text_number)

    return digits[0] * 10 + digits[-1]


def is_text_number(line: str, idx: int) -> int | None:
    search_texts = [
        ["one", 1],
        ["two", 2],
        ["three", 3],
        ["four", 4],
        ["five", 5],
        ["six", 6],
        ["seven", 7],
        ["eight", 8],
        ["nine", 9],
    ]

    for search_text in search_texts:
        if line[idx:idx + len(search_text[0])] == search_text[0]:
            return search_text[1]

    return None


def parse_input_file(file: int) -> list[str]:
    return read_input_file_id(1, file)


def level1(consider_text: bool, file: int = 0) -> int:
    lines = parse_input_file(file)
    if consider_text:
        return sum(map(process_line_with_text, lines))
    else:
        return sum(map(process_line, lines))


if __name__ == '__main__':
    print("Coordinate sum: " + str(level1(False, 2)))
    print("Coordinate sum with text: " + str(level1(True, 2)))


def test_level1():
    assert 142 == level1(False, 0)
    assert 281 == level1(True, 1)
