#Classes script for the Card deck
from CardClass import Card
import random

class Deck():

    """
    This is the Deck class for the cards in the game.
    It acts as more of a deck manager, as opposed to a deck itself
    This class is responsible for managing card objects in it

    Functions:

    generate_deck populates the local deck list
    remove_card removes the card selected and takes the suit and value as the parameter
    generate_hand generates a list which contains the hand for the player ~ takes the amount as a parameter
    find_card returns boolean depending on whether the suit and value in the parameters are found
    
    """
    def __init__(self):
        
        single_value_gen = ("2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace" )
        self.value_gen = set()
        
        #ensures that the picture cards still have a value
        for index, item in enumerate(single_value_gen):
            self.value_gen.add((item,index+2))

        self.suit_gen = (("Diamond","♦"), ("Spade","♠"),("Club","♣"),("Heart","♥"))
        self.deck = self.generate_deck()
        
    def generate_deck(self):
        """
        Logic for iterating through both lists to create a full deck of cards.
        Also resets the local deck list
        """
        self.deck = []
        for value in self.value_gen:
            for suit in self.suit_gen:
                self.deck.append(Card(suit, value))
        random.shuffle(self.deck) #always shuffle deck after generation
        

    def remove_card(self, selected_suit: str, selected_value: str):
        """
        Function for removing card from current hand
        """

        for card in self.deck:
            if card.suit[0].lower() == selected_suit.lower() and card.value[0].lower() == selected_value.lower():
                self.deck.remove(card)

    def generate_hand(self, amount) -> list:
        """
        Function which returns a list of Card objects
        This represents the hand the user has
        """

        #verify the amount of cards in the hand
        if not ((8 >= amount) and (amount >= 6)):
            raise Exception("Too many cards requested for this hand")

        hand = []
        for iteration in range(amount):
            hand.append(self.deck[0])
            self.remove_card(self.deck[0].suit[0], self.deck[0].value[0])
        return hand

    def find_card(self, selected_suit:str, selected_value:str):
        """
        Function which returns True or False to verify 
        whether the card is in the current hand
        """
        for card in self.deck:
            if (card.suit[0].lower() == selected_suit.lower()) and (card.value[0].lower() == selected_value.lower()):
                return True
        return False
