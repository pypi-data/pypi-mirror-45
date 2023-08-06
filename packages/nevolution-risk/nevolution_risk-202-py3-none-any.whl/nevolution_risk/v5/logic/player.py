import numpy as np
from numpy import float32

from nevolution_risk.constants.colors import white
from nevolution_risk.v5.logic.card_factory import Card_factory


class Player(object):
    def __init__(self, name, id=0, color=white, action_len=0, card_factory=None):
        self.name = name
        self.id = id
        self.troops = 0
        self.color = color
        self.valid_actions = np.zeros(action_len, dtype=float32)
        self.card_factory = None
        self.card_received = False

        if card_factory is None:
            self.card_factory = Card_factory()
        else:
            self.card_factory = card_factory

        self.reward = 0
        self.next_player = None
        self.lost = False
        self.cards = []

    def add_card(self):
        """
        Adds a card to the player card deck
        :return:
        """
        self.cards.append(self.card_factory.area_card())

    def combine_cards(self):
        """
        Combines player cards depending on how many of kind of cards the player holds in his deck
        :return: adds, depending on the combination, 4, 6, 8 or 10 troops to the player troops
        """
        i = 0
        c = 0
        a = 0
        for card in self.cards:
            if card.typ == 0:
                i = i + 1
            elif card.typ == 1:
                c = c + 1
            elif card.typ == 2:
                a = a + 1

        for card in self.cards:
            if i > 0 and c > 0 and a > 0:
                var1 = 1
                var2 = 1
                var3 = 1
                for ele in self.cards[:]:
                    if ele.typ == 0 and var1 != 0:
                        self.cards.remove(ele)
                        var1 = var1 - 1
                    elif ele.typ == 1 and var2 != 0:
                        self.cards.remove(ele)
                        var2 = var2 - 1
                    elif ele.typ == 2 and var3 != 0:
                        self.cards.remove(ele)
                        var3 = var3 - 1

                    if var1 == 0 and var2 == 0 and var3 == 0:
                        self.troops += 10
                        return True


            elif card.typ == 0:
                if i >= 3:
                    n = 3
                    for ele in self.cards[:]:
                        if ele.typ == 0:
                            self.cards.remove(ele)
                            n = n - 1
                            if n == 0:
                                self.troops += 4
                                return True
            elif card.typ == 1:
                if c >= 3:
                    n = 3
                    for ele in self.cards[:]:
                        if ele.typ == 1:
                            self.cards.remove(ele)
                            n = n - 1
                            if n == 0:
                                self.troops += 6
                                return True
            elif card.typ == 2:
                if a >= 3:
                    n = 3
                    for ele in self.cards[:]:
                        if ele.typ == 2:
                            self.cards.remove(ele)
                            n = n - 1
                            if n == 0:
                                self.troops += 8
                                return True
            else:
                return False
        return False

if __name__ == '__main__':
    # graph = Graph((1, 2), 4)
    # player = Player("dirk")

    # card = graph.card_fac.area_card()

    # player.add_card()
    # player.add_card()
    # player.add_card()
    # player.add_card()
    # player.add_card()

    # print("\n", player.cards, "\n")

    # print(player.combine_cards())

    # print("\n", player.cards, "\n")
    pass
