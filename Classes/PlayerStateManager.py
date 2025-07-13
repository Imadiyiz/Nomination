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
    def __init__(self, players:set):
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
            
    def update_dealer_order(self, player_queue: list):
        """
        Function for updating the dealer and changing the order of play

        Returns player queue
        """

        moving_player = player_queue[0]
        player_queue.append(moving_player)
        #should be a duplicate so first occurance is deleted
        player_queue.remove(moving_player)

        return player_queue

    def update_winner_order(self, winner:Player, player_queue:list):
        """
        Function for updating the order of the play depending on which player won the round

        Returns player queue
        """

        found = False
        while not found:
            if player_queue[0] == winner:
                found = True
                return player_queue
            selected_player = player_queue[0]
            player_queue.append(selected_player)
            player_queue.remove(selected_player)
        
        return player_queue



