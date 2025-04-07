from src.market_poker.engine import GameEngine
from src.market_poker.player import Player


if __name__ == "__main__":
    # Create players
    players = []
    done_players = False
    while not done_players:
        players.append(Player(str(input("Enter player name: "))))
        is_ready = input("    Done submitting players? (y/n): ").strip().lower()
        if is_ready == "y":
            done_players = True

    # Launch game
    engine = GameEngine(players)
    engine.run_game()
