class Option:
    def __init__(self, buyer, writer, underlying_hand, option_type, strike_price, expiry, premium, size):
        if option_type not in ["call", "put"]:
            raise ValueError("Invalid option type")
        self.buyer = buyer
        self.owner = buyer # in case the contract is sold
        self.writer = writer # pays if the option is exercized
        self.underlying_hand = underlying_hand  # will reference the player associated with the hand
        self.type = option_type # call or put
        self.strike_price = strike_price
        self.expiry = expiry  # will reference which street the option expires on (flop, river, turn)
        self.premium = premium
        self.size = size
        self.exercised = False
        self.expired = False

    def is_expired(self, current_street):
        return self.expired # remember to include a flag updater in engine.py
    
    def exercize(self, market_price): # market price determined by vwap if not river
        if self.option_type == "call":
            return max(market_price - self.strike_price, 0) * self.size
        else:
            return max(self.strike_price - market_price, 0) * self.size

"""
Idea: give players the option to "run a sim" at a cost (e.g. “Pay $1 to compute the EV of this hand”),  to reward players who invest in "research."
"""

class Option_Market:
    def __init__(self, temp):
        self.temp = temp

    def compute_vwap(spreads):
        weighted_total = 0
        total_volume = 0

        for s in spreads:
            if s.bid <= s.ask:
                midpoint = (s.bid + s.ask) / 2
                weighted_total += midpoint * s.size
                total_volume += s.size

        return weighted_total / total_volume if total_volume > 0 else None