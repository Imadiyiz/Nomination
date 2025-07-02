# Contents for the PlayerStateManager python file

from .PlayerClass import Player
from .CardClass import Card

class PlayerStateManager():
    """
    Handles actions on behalf of the player objects

    *Tracks scores
    *Updates statuses
    *Resets Players
    *QUery player hand if necessary
    """
    def __init__(self, players):
        self.players = players # list of player objects
        self.current_turn = 0

    def next_turn(self):
        """
        Determines which player's turn is next
        """
        self.current_turn = (self.current_turn + 1) % len(self.players)
        return self.player[self.current_turn]

    def add_score(self, player:Player, points: int):
        player.total_score += points

    def set_dealer(self, player:Player):
        player.dealer = True

    def get_dealer(self):
        for player in self.players:
            if player.dealer:
                return player
        return None
            



