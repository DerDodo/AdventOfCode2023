from util.file_util import read_input_file


def level15() -> tuple[int, int]:
    commands = parse_input_file()
    hash_sum = 0
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(0, 256)]
    for command in commands:
        hash_sum += calculate_hash(command)
        if command[-2] == "=":
            label = command[:-2]
            box = calculate_hash(label)
            add_to_box(boxes[box], label, int(command[-1]))
        elif command[-1] == "-":
            label = command[:-1]
            box = calculate_hash(label)
            delete_from_box(boxes[box], label)
    return hash_sum, calculate_focusing_power(boxes)


def parse_input_file() -> list[str]:
    lines = read_input_file(15)
    return lines[0].split(",")


def calculate_hash(command: str) -> int:
    result = 0
    for char in command:
        result = ((result + ord(char)) * 17 % 256)
    return result


def add_to_box(lenses: list[tuple, int], label: str, focal_value: int):
    for i, lens in enumerate(lenses):
        if lens[0] == label:
            lenses[i] = (label, focal_value)
            return
    lenses.append((label, focal_value))


def delete_from_box(lenses: list[tuple, int], label: str):
    for i, lens in enumerate(lenses):
        if lens[0] == label:
            lenses.pop(i)
            return


def calculate_focusing_power(boxes: list[list[tuple[str, int]]]) -> int:
    focusing_power = 0
    for box_i, box in enumerate(boxes):
        for lens_i, lens, in enumerate(boxes[box_i]):
            focusing_power += (box_i + 1) * (lens_i + 1) * lens[1]
    return focusing_power


if __name__ == '__main__':
    print("Sum hash: " + str(level15()))


def test_level15():
    assert (1320, 145) == level15()
