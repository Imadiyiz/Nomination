 # content of TestClass.py

from DeckClass import Deck
from CardClass import Card


#NEED TO TEST EVERY SINGLE FUNCTION FOR THE DECK
#CURRENT CAN REMOVE AND FIND CARDS IN THE DECK

class TestClass:

    def test_card(self):
        test_card = Card(("Diamond", "♦"), ("10", 10))
        assert test_card.suit == ("Diamond", "♦")
        assert test_card.value == ("10", 10)
        assert test_card.value.get("10") == 10
