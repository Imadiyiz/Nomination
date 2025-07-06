# Contents for the table class in the Nomination game

from .CardClass import Card

class Table():
    """
    Class for the table. 
    Controls the flow of actions for the current stack of cards
    Acts as a handManager

    Responsible for managing the stack of cards during the round.
    Responsible for determining which hand is won by which player
    Responsible for validating whether the hand played is valid
    """

    def __init__(self, max_players: int = 0):

        self.stack = list()
        self.winning_suit = None

    
    def display_stack(self, visual: bool = False) -> str:
        """
        Function for displaying the card contents of the current stack

        Returns a string of the stack in a readable format
        """

        if self.stack:
            string = ""
            if visual:
                for card in self.stack:
                    string += f"{card.picture}\n"
                return string
            else:
                for card in self.stack:
                    string += f"{card}\n"
                return string
        else:
            return "Stack is currently empty" 

    def add_to_stack(self, card: Card = None):
        """
        Function for adding a card to the current
         stack on the table

        Make sure to manually remove card from player hand
        """
        self.stack.append(card)

    
    def valid_add_to_stack(self, card: Card = None, trump_suit: str = None, first_card: Card = None, player_hand: list = []) -> bool:
        """
        Function for verifying whether the card is able to be played in the current deck

        Returns True if the card is valid and able to be added to the card stack
        Returns False if the card is invalid and is unable to be added to the card stack
        """

        forced = False
        #multiple iterations happen with the computer as I havent programmed sound logic for them
        if self.stack: 
            if first_card.suit:
                #determine whether they have to play a first suit/trump 
                for _card in player_hand:
                    if _card.suit[0].lower() == first_card.suit[0].lower():
                        forced = True
                if not forced:
                    return True
                #must play first card suit
                if card.suit[0].lower() == first_card.suit[0].lower():
                    return True
                else:
                    return False
        return True


    def verify_winner(self, trump_suit: str) -> Card:
        """
        Function for determining who is currently winning the stack on the table

        Must know what the trump suit is, to correctly verify the winner

        Returns the winning card
        """
        #reset winning card and suits
        winning_card = None
        trumped = False

        #quick check to verify whether the stack has been trumped
        for card in self.stack:
            if card.suit[0].lower() == trump_suit.lower():
                trumped = True

        #trumped cards are in the stack
        if trumped:
            for card in self.stack:
                if card.suit[0].lower() == trump_suit.lower():
                    if winning_card is None or card.value[1] > winning_card.value[1]:
                        winning_card = card
        else:
        #No trumps in stack
            for card in self.stack:
                if winning_card:
                    if card.suit[0].lower() == self.winning_suit.lower():
                        if card.value[1] > winning_card.value[1]:
                            winning_card = card
                else:
                    winning_card = card
                    self.winning_suit = card.suit[0].lower()
        return winning_card # will have to manually query for the owner


    def reset(self):
        """
        Function which resets the stack
        """

        self.winning_suit = None
        self.stack = list()
