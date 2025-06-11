# Contents of the Scoreboard class which keeps track of the scores in the game

from .PlayerClass import Player


class Scoreboard():
    """
    Scoreboard class used to monitor and update the scores of multiple players.
    Acts more as a manager than a storage place for the scores.

    Parameters: Accepts Player List objects only
    """

    def __init__(self, *args:list):
        self.scoreboard = {}
        self.overall_scoreboard = []
        for player_list in args: #max 6
            for player in player_list:
                self.scoreboard[player] = 0 #sets score to 0
                print("args:: ", player)
        print("scoreboard:: ",self.scoreboard)
        
    def display(self) -> list:
        """
        Function for outputting the scores in the game
        """
        return self.scoreboard
