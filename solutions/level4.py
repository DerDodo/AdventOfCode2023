from typing import Tuple

from util.file_util import read_input_file


class LotteryTicket:
    number: int
    winning_numbers: set[int]
    game_numbers: list[int]

    def __init__(self, definition: str):
        parts = definition.split(":")
        self.number = int(parts[0][5:])
        numbers = parts[1].split("|")
        self.winning_numbers = set(map(int, numbers[0].strip().replace("  ", " ").split(" ")))
        self.game_numbers = list(map(int, numbers[1].strip().replace("  ", " ").split(" ")))

    def calc_points(self) -> int:
        points = 0.49999
        for number in self.game_numbers:
            if number in self.winning_numbers:
                points *= 2
        return round(points)

    def calc_wins(self) -> int:
        points = 0
        for number in self.game_numbers:
            if number in self.winning_numbers:
                points += 1
        return round(points)


def parse_input_file() -> list[LotteryTicket]:
    return list(map(LotteryTicket, read_input_file(4)))


def level4() -> Tuple[int, int]:
    tickets = parse_input_file()
    points_per_ticket = dict(map(lambda t: (t.number, t.calc_points()), tickets))
    wins_per_ticket = dict(map(lambda t: (t.number, t.calc_wins()), tickets))
    number_of_tickets = dict(map(lambda t: (t.number, 1), tickets))
    for number, wins in wins_per_ticket.items():
        for i in range(0, min(wins, len(wins_per_ticket) - number)):
            number_of_tickets[number + i + 1] += number_of_tickets[number]
    total_points = sum(points_per_ticket.values())
    total_number_of_tickets = sum(number_of_tickets.values())
    return total_points, total_number_of_tickets


if __name__ == '__main__':
    print("Engine part sum: " + str(level4()))


def test_level4():
    assert (13, 30) == level4()
