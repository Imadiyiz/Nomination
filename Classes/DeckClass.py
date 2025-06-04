#Classes script for the Card deck
from CardClass import Card

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
        Logic for iterating through both lists to create a full deck of cards
        Also resets the local deck list
        """
        self.deck = []
        print("suit gen:: ", self.suit_gen)
        print("Value gen:: ", self.value_gen)
        for value in self.value_gen:
            for suit in self.suit_gen:
                self.deck.append(Card(suit, value))

    def remove_card(self, suit: str, value: str):
        """
        Function for adding a card back to the deck when necessary
        """
        for card in self.deck:
            if card.suit[0].lower() == suit.lower() and card.value[0].lower() == value.lower():
                self.deck.remove(card)
        print(len(self.deck))
    
    def find_card(self, suit:str, value:str):
        """
        Function which returns True or False to verify 
        whether the card is in the deck
        """
        for card in self.deck:
            if card.suit[0].lower() == suit.lower() and card.value[0].lower() == value.lower():
                return True
        return False
        
        
lol = Deck()

lol.generate_deck()
#lol.remove_card("Diamond", "5")
#print(lol.find_card("Diamond", "10"))


test_card = Card(("Diamond", "♦"), ("10", 5))
