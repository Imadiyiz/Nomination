 # content of TestClass.py

from DeckClass import Deck
from CardClass import Card
from PlayerClass import Player
from ScoreboardClass import Scoreboard
import pytest


#NEED TO TEST EVERY SINGLE FUNCTION FOR THE DECK
#CURRENT CAN REMOVE AND FIND CARDS IN THE DECK

# ALL TESTS MUST START WITH THE 'TEST' PREFIX

class TestClass:

    """Class for checking the assigning of the cards"""

    def test_card_owner(self):
        myplayer = Player()
        test_card = Card(("Diamond", "♦"), ("10", 10), myplayer)
        assert test_card.owner == myplayer


    def test_card(self):
        test_card = Card(("Diamond", "♦"), ("10", 10))
        assert test_card.suit == ("Diamond", "♦")
        assert test_card.value == ("10", 10)
        assert test_card.value[1] == 10
    
# Do not need to keep repeating the initialisation of the Deck object   
@pytest.fixture 
def my_deck():
    deck = Deck()
    deck.generate_deck() #generates full deck
    return deck
    

class TestDeckClass:

    """
    Class for testing the functionality of the DeckManager class
    """

    def test_deck_generation(self, my_deck):
        assert len(my_deck.deck) == 52
        assert type(my_deck.deck) == list

    def test_deck_card_find(self,my_deck):
        assert my_deck.find_card("Spade", "5") == True
        assert my_deck.find_card("Heart", "5") == True
        assert my_deck.find_card("Club", "5") == True
        assert my_deck.find_card("Diamond", "5") == True
        assert my_deck.find_card("Spacee", "ace") == False
        assert my_deck.find_card("club", "Jack") == True
        assert my_deck.find_card("spade", "Qeeun") == False
        assert my_deck.find_card("Heart", "14") == False
        assert my_deck.find_card("diamonD", "15") == False
        assert my_deck.find_card("clubs", "Twelve") == False

    def test_card_removal(self, my_deck): 
        my_deck.remove_card("Diamond", "10")
        my_deck
        assert my_deck.find_card("Diamond", "10") == False
    

class TestScoreboardClass():
    """
    Class for testing the functionality of the Scoreboard class
    """

    def test_scoreboard_generation(self):
        player1 = Player()
        player2 = Player()
        player3 = Player()
        player4 = Player()
        my_scoreboard=Scoreboard(player1,player2,player3,player4)
        assert type(my_scoreboard.display()) == dict
        
