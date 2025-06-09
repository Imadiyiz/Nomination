# Contents of the Scoreboard class which keeps track of the scores in the game

from PlayerClass import Player


class Scoreboard():
    """
    Scoreboard class used to monitor and update the scores of multiple players.
    Acts more as a manager than a storage place for the scores.

    Parameters: Accepts Player objects only
    """

    def __init__(self, *args):
        self.scoreboard = {}
        for player in args[:5]: #max 6
            self.scoreboard[str(player)] = 0 #sets score to 0
            print("args:: ", player)
        print("scoreboard:: ",self.scoreboard)
        
    def display(self) -> list:
        """
        Function for outputting the scores in the game
        """
        print(self.scoreboard)
        return self.scoreboard
        

myplayer = Player()
myplayer2 = Player()
myplayer3 = Player()
myscoreboard = Scoreboard(myplayer, myplayer2, myplayer3)
myscoreboard.display()
