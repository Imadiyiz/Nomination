#Classes script for the Card deck
import pytest
from Card import Card

class Deck():

    """
    This is the Deck class for the cards in the game.
    It acts as more of a deck manager, as opposed to a deck itself
    This class is responsible for managing card objects in it

    Functions:

    generate_deck populates the local deck list
    
    """
    def __init__(self):
        
        single_value_gen = (2,3,4,5,6,7,8,9,10,"Jack","Queen","King","Ace" )
        self.value_gen = {}
        for index, item in enumerate(single_value_gen):
            self.value_gen.update({item:index+2})
        self.suit_gen = ({"Diamond":"♦"},{"Spades":"♠"},{"Club":"♣"}, {"Heart":"♥"})
        self.deck = []
        
    def generate_deck(self):
        """
        Logic for iterating through both lists to create a full deck of cards
        Also resets the local deck list
        """
        self.deck = []
        for value in self.value_gen.keys():
            for suit in self.suit_gen:
                self.deck.append(Card(suit,value))

    def add_card(self, suit: dict, value: dict):
        """
        Function for adding a card back to the deck when necessary
        """
        
        return
        
lol = Deck()

lol.generate_deck()

mydeck = lol.deck

for item in mydeck:
    print(item)
print(len(mydeck))