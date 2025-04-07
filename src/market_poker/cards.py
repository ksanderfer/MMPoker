from treys import Deck as Tdeck, Evaluator

class Deck:
    def __init__(self):
        self.deck = Tdeck()
        self.community_cards = []

    def deal_hole(self, players: list):
        for player in players:
            for _ in range(2):
                player.hole_cards.append(self.deck.draw)

    def deal_community(self, street: str):
        if street == "flop":
            for _ in range (4):
                self.community_cards.append(self.deck.draw)

        elif street == "turn":
            self.community_cards.append(self.deck.draw)

        else:
            raise ValueError("Invalid street type")

    def evaluate_hands(self, players: list):
        for player in players:
            evaluator = Evaluator()
            hand_strengths = {
                p: evaluator.evaluate(self.community_cards, p.hole_cards)
                for p in players
            }
        return sorted(hand_strengths.items(), key=lambda x: x[1])

