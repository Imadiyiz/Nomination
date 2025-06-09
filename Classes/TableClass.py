# Contents for the table class in the Nomination game

import queue
from CardClass import Card

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

    def __init__(self, max_players: int = 0):

        self.stack = queue.Queue()
        self.stack.maxsize(max_players)
    
    def display_stack(self):
        """
        Function for displaying the card contents of the current stack
        """

        for card in self.stack:
            print(card)

    def add_to_stack(self, card: Card = None):
        """
        Function for adding a card to the current stack on the table
        """
        if card not in self.stack:
            self.stack.put(card)
            return
        raise Exception("Duplicate card added to the stack")

    def verify_winner(self, trump_suit: str):
        """
        Function for determining who is currently winning the stack on the table

        Must know what the trump suit is, to correctly verify the winner

        Returns the owner of the winning card
        """
        #reset winning card and suits
        winning_card = None
        winning_suit = None
        trumped = False

        #quick check to verify whether the stack has been trumped
        for card in self.stack:
            if card.suit[0].lower() == trump_suit:
                trumped = True
            break

        #trumped cards are in the stack
        for card in self.stack:
            if trumped:
                if card.suit[0] == trump_suit.lower():
                    if winning_card == None:
                        winning_card = card
                    
                    elif card.value[1] > winning_card.value[1]:
                            winning_card = card
        
        #no trump cards in stack

        for card in self.stack:
            #if there is no winning card then the first card is the winning card
            if winning_card:

                #if current card's suit is the same as winning_suit
                if card.suit[0].lower() == winning_suit:
                    if card.value[1] > winning_card.value[1]:
                        winning_card = card
            else:
                winning_card = card
                winning_suit = card.suit[0].lower()

        return winning_card.owner


        