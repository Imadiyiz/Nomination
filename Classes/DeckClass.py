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
    
    """
    def __init__(self):
        
        single_value_gen = ("2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace" )
        self.value_gen = set()
        
        #ensures that the picture cards still have a value
        for index, item in enumerate(single_value_gen):
            self.value_gen.add((item,index+2))

        self.suit_gen = (("Diamond","♦"), ("Spade","♠"),("Club","♣"),("Heart","♥"))
        self.deck = []
        
    def generate_deck(self):
        """
        Logic for iterating through both lists to create a full deck of cards.
        Also resets the local deck list
        """
        self.deck = []
        print("suit gen:: ", self.suit_gen)
        print("Value gen:: ", self.value_gen)
        for value in self.value_gen:
            for suit in self.suit_gen:
                self.deck.append(Card(suit, value))
    
    def shuffle_deck(self):
        """
        Function to shuffle the items in the deck
        """
        random.shuffle(self.deck)

    def remove_card(self, selected_suit: str, selected_value: str):
        """
        Function for removing card from current hand
        """

        for card in self.deck:
            if card.suit[0].lower() == selected_suit.lower() and card.value[0].lower() == selected_value.lower():
                self.deck.remove(card)

    def generate_hand(self, amount):
        """
        Function which returns a list of Card objects
        This represents the hand the user has
        """
        hand = []
        for iteration in range(amount):
            hand.append(self.deck[0])
            self.remove_card(self.deck[0].suit[0], self.deck[0].value[0])
        for card in hand:
            print(card)
    
        
lol = Deck()

#perfect
lol.generate_deck()
lol.shuffle_deck()
lol.generate_hand(8)


test_card = Card(("Diamond", "♦"), ("10", 5))
