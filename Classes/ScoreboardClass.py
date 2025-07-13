# Contents of the Scoreboard class which keeps track of the scores in the game

from .PlayerClass import Player


class Scoreboard():
    """
    Scoreboard class used to monitor and update the scores of multiple players.
    Acts more as a manager than a storage place for the scores.

    Parameters: Accepts Player List objects only
    """

    def __init__(self, *args:list):
        self.round_scoreboard = {}
        self.total_scoreboard = []
        for player_list in args: #max 6
            for player in player_list:
                self.round_scoreboard[player.name] = 0 #sets score to 0


        
    def display(self, round: int = True) -> list:
        """
        Function for outputting the scores in the game

        Returns a formatted version of the scoreboard which is readable 
        """
        

        formatted_scoreboard = []
        for player, value in self.round_scoreboard.items():
            formatted_scoreboard.append((player,value))
        
        if not round:
           for player, value in self.total_scoreboard.items():
            formatted_scoreboard.append((player,value)) 

        return formatted_scoreboard
    
    def update_round_scoreboard(self, player_list:list, winner_card):
        """
        Updates the round scoreboard using the player bids and the player score from the round
        """
        #update round score winner 
        for _player in player_list:
            if _player == winner_card.owner:
                _player.round_score +=1 
                self.round_scoreboard[_player.name] = _player.round_score
    
    def update_total_scoreboard(self, player_list:list, max_cards: int = 8):
        """
        Updates the total scoreboard using the player bids and the player score from the round
        """

        for _player in player_list:
            #check if they got their score correct
            if _player.bid == max_cards and _player.round_score == _player.bid:
                self.total_scoreboard[_player.name] += (_player.bid + 10)*2

            if _player.bid == _player.round_score:
                self.total_scoreboard[_player.name] += _player.bid + 10
            else:
                self.total_scoreboard[_player.name] += _player.round_score

    def reorder_round_scoreboard(self, player_queue:list):
        """
        Reorders the round scoreboard to ensure it aligns with the current bids

        Args:
            player_queue (list): The player queue is necessary to preserve the correct order
        """

        temp_dict = {}
        for player in player_queue:
            temp_dict[player.name] = player.round_score
        self.round_scoreboard = temp_dict
