from src.market_poker.cards import *
from src.market_poker.market import *
from src.market_poker.option import *
from src.market_poker.player import *
from collections import defaultdict
from treys import Card
import time

class GameEngine:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.spreadbook = SpreadBook()
        self.options = []
        self.market_prices = defaultdict(float) # {hand_id : price}

    def run_game(self):
        while len(self.players) > 1:
            # Get new deck, deal and view cards
            self.deck = Deck()
            self.deck.deal_hole(self.players)
            for player in self.players:
                print(f"{player.name}'s hand: ", end="")
                Card.print_pretty_cards(player.hole_cards)

            for street in ["preflop", "flop", "turn"]:
                if street != "preflop":
                    self.deck.deal_community(street)
                    print(f"\n{street.title()}: ", end="")  # Use title case for nicer formatting
                    Card.print_pretty_cards(self.deck.community_cards)
                for player in self.players:
                    player.not_ready()
                self.submit_spreads()
                self.market_prices = self.spreadbook.get_all_prices()
                if not street == "preflop":
                    self.allow_early_exercise(street)
                # allow option trading here
                self.order_match()
                
            self.deck.deal_community("river")
            print(f"River: ", end="")
            Card.print_pretty_cards(self.deck.community_cards)
            self.settle_game()

    def order_match(self):
        print("\n---Matching orders---")

        for hand_id in self.spreadbook.book:
            bids = sorted([spread for spread in self.spreadbook.get_spreads(hand_id) if spread.bid > 0],
                          key=lambda spread: -spread.bid)
            
            asks = sorted([spread for spread in self.spreadbook.get_spreads(hand_id) if spread.ask > 0],
                          key= lambda spread: spread.ask)
            
            while bids and asks and bids[0].bid >= asks[0].ask:
                buyer = bids[0].player
                seller = asks[0].player
                trade_quantity = min(bids[0].size, asks[0].size)
                trade_price = (bids[0].bid + asks[0].ask) / 2

                # Execute trade
                total_cost = trade_price * trade_quantity
                if buyer.buy(hand_id, trade_price, trade_quantity) and seller.sell(hand_id, trade_price, trade_quantity):
                    time.sleep(0.5)
                    print(f"{buyer} bought {trade_quantity} shares of {hand_id} at {trade_price: .2f} from {seller}. Total cost = {total_cost: .2f} chips")
                elif not buyer.buy(hand_id, trade_price, trade_quantity):
                    bids.pop(0)
                    continue
                else:
                    asks.pop(0)
                    continue

                # Update sizes, remove filled orders
                bids[0].size -= trade_quantity
                asks[0].size -= trade_quantity
                if bids[0].size == 0:
                    bids.pop(0)
                if asks[0].size == 0:
                    asks.pop(0)



    def submit_spreads(self):
        print("\n--- Market Making Phase ---")

        while True:
            num_unchanged = 0  # Tracks players who made no changes this round

            for player in self.players:
                spread_changed = False

                if player.ready:
                    print(f"{player.name} has marked themselves ready to move to the next street. Skipping...")
                    num_unchanged += 1
                    continue

                print(f"\n{player.name}, submit your spreads:")

                for target_player in self.players:
                    hand_id = target_player.name
                    print(f"  Submit a new spread on {hand_id}'s hand?")
                    Card.print_pretty_cards(target_player.hole_cards)
                    will_submit = input("    Type y/n: ").strip().lower()

                    if will_submit != "y":
                        continue
                    
                    self.view_market(hand_id)

                    try:
                        bid = float(input("    Bid: "))
                        ask = float(input("    Ask: "))
                        size = int(input("    Size: "))
                    except ValueError:
                        print("    Invalid input, skipping this spread.")
                        continue

                    if bid > ask:
                        print("    Invalid spread: bid cannot exceed ask.")
                        continue

                    spread = Spread(player, hand_id, bid, ask, size)
                    self.spreadbook.add_spread(spread)
                    spread_changed = True

                # Ask if player wants to mark as ready
                is_ready = input("    Ready for next street? (y/n): ").strip().lower()
                if is_ready == "y":
                    player.ready = True

                if not spread_changed:
                    num_unchanged += 1

            # End loop if all players made no changes
            if num_unchanged == len(self.players):
                print("\nNo changes from any player. Ending market making phase.")
                break


    def allow_early_exercise(self, street):
        pass

    def view_market(self, hand_id):
        print(f"\nCurrent market for {hand_id}'s hand:")

        price = self.spreadbook.compute_vwap(hand_id)
        if price is not None:
            print(f"  Market Price (VWAP): {price:.2f} chips")
        else:
            print("  Not enough info to determine market price.")

        spreads = self.spreadbook.get_spreads(hand_id)
        if spreads:
            for spread in spreads:
                if not spread == None:
                    print(f"    {spread.player.name}: Bid = {spread.bid:.2f} chips, Ask = {spread.ask:.2f} chips, Size = {spread.size}")
                else:
                    print(f"    {spread.player.name} has not submitted a spread on this hand.")
            print(f"    Best bid: {self.spreadbook.get_best_bid(hand_id)}, best ask: {self.spreadbook.get_best_ask(hand_id)}")
        else:
            print("    No spreads submitted.")


    def settle_game(self):
        winning_hand_id = self.deck.evaluate_hands(self.players)[0][0]
        for player in self.players:
            for hand_id in player.owned:
                if hand_id == winning_hand_id:
                    net_profit = (player.owned[hand_id] * 100)
                    player.chips += net_profit
                    if net_profit > 0:
                        print(f"{player.name} earned {net_profit} chips")
                    if net_profit < 0:
                        print(f"{player.name} lost {net_profit} chips")
        eliminated = [p for p in self.players if p.chips <= 0]
        for p in eliminated:
            print(p.name + " was eliminated")
            self.players.remove(p)