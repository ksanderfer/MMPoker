from collections import defaultdict
from src.market_poker.market import Spread

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hole_cards = []
        self.chips = 1000
        self.spreads = defaultdict(Spread) # {street: Spread}
        self.options = []
        self.owned =  defaultdict(int) # {hand_id: size}
        self.ready = False # flag indicating if user is ready to proceed to next street

    def __str__(self):
        return self.name

    def ready_true(self):
        self.ready = True

    def not_ready(self):
        self.ready = False

    def buy(self, hand_id, price, size):
        if (price * size) <= self.chips:
            self.owned[hand_id] += size
            self.chips -= (price * size)
            return True
        else:
            print("Insufficient balance to purchase")
            return False

    def sell(self, hand_id, price, size):
        if (size * 100) <= self.chips: # Must be able to cover collateral
            self.owned[hand_id] -= size
            self.chips += size * price
            return True
        else:
            print("Insufficient balance to cover risk")
            return False

    