from util.file_util import read_input_file


class Container:
    text: str

    def __init__(self, text: str):
        self.text = text


def parse_input_file() -> Container:
    return Container(read_input_file(0)[0])


def level0() -> Container:
    return parse_input_file()


if __name__ == '__main__':
    print("The message: " + level0().text)


def test_level1():
    assert "Dodo ist da!" == level0().text
