class Player:
    def __init__(self, name: str):
        self.name = name
        self.hole_cards = []
        self.chips = 1000
        self.spreads = {} # {street: Spread}
        
class Spread:
    def __init__(self, player, hand_id, bid, ask, size=1):
        self.player = player
        self.hand_id = hand_id # will probably be the player name associated with the hand
        self.bid = bid
        self.ask = ask
        self.size = size  # Number of contracts or volume