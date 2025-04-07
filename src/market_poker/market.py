from collections import defaultdict

class Spread:
    def __init__ (self, player, hand_id, bid, ask, size):
        self.player = player
        self.hand_id = hand_id
        self.bid = bid
        self.ask = ask
        self.size = size

class SpreadBook:
    def __init__ (self):
        self.book = defaultdict(list)

    def add_spread(self, spread: Spread):
        """Add a new spread to the order book."""
        self.book[spread.hand_id].append(spread)

    def get_spreads(self, hand_id):
        """Return all spreads on a specific hand."""
        return self.book.get(hand_id, [])

    def remove_spreads_by_player(self, player):
        """Remove all spreads submitted by a player."""
        for hand_id in self.book:
            self.book[hand_id] = [
            spread for spread in self.book[hand_id] if spread.player != player
        ]

    def compute_vwap(self, hand_id):
        """Compute the volume-weighted average price for a given hand."""
        spreads = self.get_spreads(hand_id)
        weighted_total = 0
        total_volume = 0

        for spread in spreads:
            if spread.bid <= spread.ask:
                midpoint = (spread.bid + spread.ask) / 2
                weighted_total += midpoint * spread.size
                total_volume += spread.size

        return weighted_total / total_volume if total_volume > 0 else None

    def get_all_prices(self):
        """Return a dict of all market prices per hand."""
        return {hand_id : self.compute_vwap(hand_id) for hand_id in self.book}


    def get_best_bid(self, hand_id):
        """Return the highest bid for the specified hand."""
        return max(spread.bid for spread in self.book[hand_id])

    def get_best_ask(self, hand_id):
        """Return the lowest ask for the specified hand."""
        return min(spread.ask for spread in self.book[hand_id])
    
    def get_player_spreads(self, player):
        """Return all spreads submitted by a player."""
        player_spreads = []

        for hand_id in self.book:
            for spread in self.book[hand_id]:
                if spread.player == player:
                    player_spreads.append(spread)

        return player_spreads

class Option_Market:
    def __init__(self, temp):
        self.temp = temp