# Contents of the Player class python file

from CardClass import Card
from DeckClass import Deck

class Player():
    """
    Class for the Player's attributes and deck

    Functions:

    Collect_deck: Assigns a deck list to the player instance
    remove_card: 
    find_card: Returns Boolean value of whether the selected card is present in the player's deck
    """

    def __init__(self, name = "AI", total_score = 0, round_score = 0, trump_decider = False, dealer = False, computer: bool = True):
        self.name = name
        self.total_score = total_score
        self.round_score = round_score
        self.trump_decider = trump_decider
        self.dealer = dealer
        self.computer = computer
        self.hand = []
        self.bid = 0

    def collect_hand(self, hand: list):
        """
        Function for receiving hand from the DeckManager
        """
        for card in hand: # assigns self as the owner to each card
            card.owner = self

        self.hand = hand 

    def discard_hand(self):
        """
        Function for discarding/resetting current hand
        """
        self.hand = []

    def remove_card(self, selected_suit: str, selected_value: str):
        """
        Function for removing card from current hand
        """

        for card in self.hand:
            if card.suit[0].lower() == selected_suit.lower() and card.value[0].lower() == selected_value.lower():
                self.hand.remove(card)

    def find_card(self, selected_suit:str, selected_value:str):
        """
        Function which returns True or False to verify 
        whether the card is in the current hand
        """
        for card in self.hand:
            if card.suit[0].lower() == selected_suit.lower() and card.value[0].lower() == selected_value.lower():
                return True
        return False

    def set_trump_decider(self, boolean: bool):
        """
        Function for setting the trump decider value
        """
        self.trump_decider = boolean

    def set_dealer(self):
        """
        Function for setting the player as the dealer
        """
        self.dealer = True

    def reset_bid(self):
        """
        Function for resetting the bidding value
        """
        self.bid = 0

    def reset_dealer_trump_decider(self):
        """
        Function for resetting both values of the trump decider and the dealer
        """

        self.dealer = False
        self.trump_decider = False

    def __str__(self):
        return self.name    

