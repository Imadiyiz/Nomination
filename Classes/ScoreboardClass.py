# Contents of the Scoreboard class which keeps track of the scores in the game

from PlayerClass import Player


class Scoreboard():
    """
    Scoreboard class used to monitor and update the scores of multiple players.
    Acts more as a manager than a storage place for the scores
    """

    def __init__(self, *args, **kwargs):
        self.scoreboard = {}
        for player in kwargs:
            self.scoreboard[player]=0
        
    def display(self):
        """
        Function for outputting the scores in the game
        """

        print(self.scoreboard)
        