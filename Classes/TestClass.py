 # content of TestClass.py

from DeckClass import Deck
from CardClass import Card


#NEED TO TEST EVERY SINGLE FUNCTION FOR THE DECK
#CURRENT CAN REMOVE AND FIND CARDS IN THE DECK

class TestClass:

    """Class for checking the assigning of the cards"""

    def test_card(self):
        test_card = Card(("Diamond", "♦"), ("10", 10))
        assert test_card.suit == ("Diamond", "♦")
        assert test_card.value == ("10", 10)
        assert test_card.value[1] == 10

class DeckTestClass:

    """
    Class for testing the functionality of the DeckManager class
    """

    def test_deck_generation(self):
        my_deck = Deck()
        my_deck.generate_deck() # generates full deck
        assert len(my_deck) == 52
        assert type(my_deck) == list

    def test_deck_generation(self): 
        my_deck = Deck()
        my_deck.generate_deck() # generates full deck
        my_deck.remove_card("Diamond", "10")
        my_card = Card((),())
        assert my_deck
    