# Contents for the table class in the Nomination game

from collections import deque

class Table():
    """
    Class for the table. 
    Controls the flow of actions for the rounds being played on the table
    Acts as a handManager

    Responsible for managing the stack of cards during the round.
    Responsible for determining which hand is won by which player
    Responsible for outputting who is currently winning the round
    Responsible for validating whether the hand played is valid
    Responsible for returning the scores to the scoreboard instance
    """

    def __init__(self):

        self.stack = deque()
    
    def display_stack(self):
        """
        Function for displaying the card contents of the current stack
        """

        for card in self.stack:
            print(card)