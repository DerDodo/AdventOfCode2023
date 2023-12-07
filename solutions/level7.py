from enum import Enum

from util.file_util import read_input_file


class Card(Enum):
    CA = (14, "A")
    CK = (13, "K")
    CQ = (12, "Q")
    CJ = (11, "J")
    CT = (10, "T")
    C9 = (9, "9")
    C8 = (8, "8")
    C7 = (7, "7")
    C6 = (6, "6")
    C5 = (5, "5")
    C4 = (4, "4")
    C3 = (3, "3")
    C2 = (2, "2")

    def from_card(card: str):
        for c in Card:
            if card == c.value[1]:
                return c

    def get_value(self, joker: bool) -> int:
        if self.value[0] == 11 and joker:
            return 1
        else:
            return self.value[0]

    from_card = staticmethod(from_card)


class Play(Enum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1

    def from_hand(hand: str, joker: bool):
        amounts = {card.value[1]: 0 for card in Card}
        for card in hand:
            amounts[card] += 1

        num_jokers = 0
        if joker:
            num_jokers = amounts.pop(Card.CJ.value[1])

        amount_list = list(amounts.values())
        if num_jokers == 5 or amount_list.count(5 - num_jokers) == 1:
            return Play.FiveOfAKind
        elif amount_list.count(4 - num_jokers) >= 1:
            return Play.FourOfAKind
        elif amount_list.count(3) == 1 and amount_list.count(2) == 1:
            return Play.FullHouse
        elif num_jokers == 1 and amount_list.count(2) == 2:
            return Play.FullHouse
        elif amount_list.count(3 - num_jokers):
            return Play.ThreeOfAKind
        elif amount_list.count(2) == 2:
            # not possible with jokers
            return Play.TwoPair
        elif amount_list.count(2) == 1 or num_jokers == 1:
            return Play.OnePair
        else:
            return Play.HighCard

    from_hand = staticmethod(from_hand)


class Bid:
    hand: str
    amount: int
    score: int

    def __init__(self, definition: str, joker: bool):
        parts = definition.split(" ")
        self.hand = parts[0]
        self.amount = int(parts[1])
        self.score = Play.from_hand(self.hand, joker).value
        for card in self.hand:
            self.score = self.score * 100 + Card.from_card(card).get_value(joker)


def level7(joker: bool) -> int:
    bids = parse_input_file(joker)
    bids.sort(key=lambda b: b.score)
    total_winnings = 0
    for idx, bid in enumerate(bids):
        total_winnings += bid.amount * (idx + 1)
    return total_winnings


def parse_input_file(joker: bool) -> list[Bid]:
    lines = read_input_file(7)
    return list(map(lambda line: Bid(line, joker), lines))


if __name__ == '__main__':
    print("Total winnings: " + str(level7(False)))
    print("Total joker winnings: " + str(level7(True)))


def test_level7():
    assert 6440 == level7(False)
    assert 5905 == level7(True)
