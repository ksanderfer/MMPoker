from treys import Deck as Tdeck, Evaluator

class Deck:
    def __init__(self):
        self.deck = Tdeck()
        self.community_cards = []

    def deal_hole(self, players: list):
        for player in players:
            player.hole_cards = self.deck.draw(2)

    def deal_community(self, street: str):
        if street == "flop":
            self.community_cards += self.deck.draw(3)
        elif street == "turn":
            self.community_cards.append(self.deck.draw(1)[0])
        elif street == "river":
            self.community_cards.append(self.deck.draw(1)[0])
        else:
            raise ValueError("Invalid street")

    def evaluate_hands(self, players: list):
        for player in players:
            evaluator = Evaluator()
            hand_strengths = {
                p: evaluator.evaluate(self.community_cards, p.hole_cards)
                for p in players
            }
        return sorted(hand_strengths.items(), key=lambda x: x[1])

